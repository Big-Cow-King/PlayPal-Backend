from django.test import TestCase, Client

from accounts.tests import login
from events.tests import create_event, update_event, join_event


# Create your tests here.
class PaymentTest(TestCase):
    def test_create_payment(self):
        client = Client()
        token = login(client)
        create_event(client, token)
        response = client.post('/payments/create/',
                               data={
                                   'event_id': '1',
                                   'amount': 100,
                                   'return_url': 'http://localhost:8000/payments/verify/',
                                      'cancel_url': 'http://localhost:8000/payments/cancel/',
                               },
                               headers={'Authorization': f'Bearer {token}'},
                               content_type='application/json',
                               )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'CREATED')

    def test_verify_payment(self):
        client = Client()
        token = login(client)
        create_event(client, token)
        response = client.post('/payments/create/',
                               data={
                                   'event_id': '1',
                                   'amount': 100,
                                   'return_url': 'http://localhost:8000/payments/verify/',
                                      'cancel_url': 'http://localhost:8000/payments/cancel/',
                               },
                               headers={'Authorization': f'Bearer {token}'},
                               content_type='application/json',
                               )
        order_id = response.data['id']
        response = client.get(f'/payments/verify/?token={order_id}',
                              headers={'Authorization': f'Bearer {token}'},
                              content_type='application/json',
                              )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'CREATED')

