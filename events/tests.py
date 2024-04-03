from django.test import TestCase, Client
from accounts.tests import login


# Create your tests here.
def create_event(client, token):
    response = client.post('/events/create/',
                           data={
                               'title': 'Event 1',
                               'description': 'Event 1 Description',
                               'visibility': 'Public',
                               'max_players': 10,
                               'start_time': '2025-01-01T00:00:00Z',
                               'end_time': '2025-01-02T01:00:00Z',
                               'content': 'Event 1 Content',
                               'sport_data': 'asd',
                               'location': 'Event 1 Location',
                               'level': 'B',
                               'age_group': 'S',
                           },
                           headers={'Authorization': f'Bearer {token}'},
                           content_type='application/json',
                           )
    return response


def update_event(client, token):
    response = client.patch('/events/update/',
                            data={
                                'id': '1',
                                'title': 'Event 1 Updated Title',
                            },
                            headers={'Authorization': f'Bearer {token}'},
                            content_type='application/json',
                            )
    return response


def join_event(client, token):
    create_event(client, token)
    response = client.patch('/events/join/',
                            data={
                                'id': '1',
                            },
                            headers={'Authorization': f'Bearer {token}'},
                            content_type='application/json',
                            )
    return response


class EventTest(TestCase):

    def test_create_event(self):
        client = Client()
        token = login(client)
        response = create_event(client, token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Event 1')

    def test_list_event(self):
        client = Client()
        response = client.get('/events/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_event(self):
        client = Client()
        response = client.get('/events/1/')
        self.assertEqual(response.status_code, 404)

    def test_update_event(self):
        client = Client()
        token = login(client)
        create_event(client, token)
        response = update_event(client, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Event 1 Updated Title')

    def test_delete_event(self):
        client = Client()
        token = login(client)
        create_event(client, token)
        response = client.delete('/events/delete/',
                                 data={
                                     'id': '1',
                                 },
                                 headers={'Authorization': f'Bearer {token}'},
                                 content_type='application/json',
                                 )
        self.assertEqual(response.status_code, 204)

    def test_join_event(self):
        client = Client()
        token = login(client)
        response = join_event(client, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('ascii'),
                         '{"message": "Joined event successfully!"}')

    def test_leave_event(self):
        client = Client()
        token = login(client)
        join_event(client, token)
        response = client.patch('/events/quit/',
                                data={
                                    'id': '1',
                                },
                                headers={'Authorization': f'Bearer {token}'},
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('ascii'),
                         '{"message": "Left event successfully!"}')
