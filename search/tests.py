from django.test import TestCase, Client

from accounts.tests import login
from events.tests import create_event
# Create your tests here.
class SearchTest(TestCase):
    def test_search_event(self):
        client = Client()
        token = login(client)
        create_event(client, token)
        response = client.get('/search/events/?search=Event 1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Event 1')
