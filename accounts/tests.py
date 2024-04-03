from django.test import TestCase, Client


# Create your tests here.
def login(client):
    client.post('/accounts/register/', {
        'username': 'daniuwang',
        'email': 'daniuwang@email.com',
        'password': 'daniuwang123',
    })

    jwt = client.post('/accounts/login/', {
        'username': 'daniuwang',
        'password': 'daniuwang123',
    })
    return jwt.data['access']


class AccountTest(TestCase):

    def test_signup(self):
        client = Client()

        # Test Successful Signup
        response = client.post('/accounts/register/', {
            'username': 'daniuwang',
            'email': 'daniuwang@email.com',
            'password': 'daniuwang123',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'daniuwang')
        self.assertEqual(response.data['email'], 'daniuwang@email.com')

        # Test Signup with existing username and email
        response = client.post('/accounts/register/', {
            'username': 'daniuwang',
            'email': 'daniuwang@email.com',
            'password': 'daniuwang123',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0].title(),
                         'This Field Must Be Unique.')
        self.assertEqual(response.data['email'][0].title(),
                         'This Field Must Be Unique.')

        # Test Invalid Password
        response = client.post('/accounts/register/', {
            'username': 'daniuwang2',
            'email': 'daniuwang2@email.com',
            'password': '123',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0].title(),
                         'This Password Is Too Short. It Must Contain At Least 8 Characters.')
        self.assertEqual(response.data['password'][1].title(),
                         'This Password Is Too Common.')
        self.assertEqual(response.data['password'][2].title(),
                         'This Password Is Entirely Numeric.')

    def test_user_view(self):
        client = Client()

        client.post('/accounts/register/', {
            'username': 'daniuwang',
            'email': 'daniuwang@email.com',
            'password': 'daniuwang123',
        })

        response = client.get('/accounts/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'daniuwang')
        self.assertEqual(response.data['email'], 'daniuwang@email.com')

        response = client.get('/accounts/2/')
        self.assertEqual(response.status_code, 404)

    def test_user_update(self):
        client = Client()
        token = login(client)

        response = client.patch('/accounts/editprofile/',
                              data={
                                  'name': 'Daniu Wang'
                              },
                              headers={'Authorization': f'Bearer {token}'},
                              content_type='application/json',
                              )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Daniu Wang')
