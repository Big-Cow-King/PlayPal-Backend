from django.test import TestCase, Client

from accounts.tests import login
from events.tests import create_event, update_event, join_event


# Create your tests here.
class NotificationTest(TestCase):
    def join_and_update_event(self, client, token):
        create_event(client, token)
        join_event(client, token)
        update_event(client, token)

    def test_get_notification(self):
        client = Client()
        token = login(client)
        self.join_and_update_event(client, token)
        response = client.get('/notifications/list/',
                              headers={'Authorization': f'Bearer {token}'},
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_read_notification(self):
        client = Client()
        token = login(client)
        self.join_and_update_event(client, token)
        response = client.get('/notifications/list/',
                              headers={'Authorization': f'Bearer {token}'},
                              content_type='application/json')
        notification_id = response.data['results'][0]['id']
        response = client.patch('/notifications/read/',
                                data={
                                    'id': notification_id,
                                },
                                headers={'Authorization': f'Bearer {token}'},
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['read'], True)

    def test_delete_notification(self):
        client = Client()
        token = login(client)
        self.join_and_update_event(client, token)
        response = client.get('/notifications/list/',
                              headers={'Authorization': f'Bearer {token}'},
                              content_type='application/json')
        notification_id = response.data['results'][0]['id']
        response = client.delete('/notifications/delete/',
                                 data={
                                     'id': notification_id,
                                 },
                                 headers={'Authorization': f'Bearer {token}'},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 204)
        response = client.get('/notifications/list/',
                              headers={'Authorization': f'Bearer {token}'},
                              content_type='application/json')
        self.assertEqual(len(response.data['results']), 0)
