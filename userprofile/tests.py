from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profile


class ProfileUpdateAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and associated profile
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone_no='1234567890', age=25)

        # URL for the edit profile endpoint
        self.url = reverse('edit_profile_api')

    def test_successful_profile_update(self):
        # Ensure the user is authenticated for the test
        self.client.force_authenticate(user=self.user)

        # Data to update
        data = {
            'phone_no': '0987654321',
            'age': 26,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the profile from the database and check the updated fields
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_no, data['phone_no'])
        self.assertEqual(self.profile.age, data['age'])

    def test_successful_profile_update_all_fields(self):
        self.client.force_authenticate(user=self.user)

        # Data to update all fields
        data = {
            'phone_no': '0987654321',
            'age': 26,
            'gender': 'Other',
            'sports_you_can_play': 'Tennis, Badminton',
            'description': 'Updated profile description.',
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the profile from the database and check the updated fields
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_no, data['phone_no'])
        self.assertEqual(self.profile.age, data['age'])
        self.assertEqual(self.profile.gender, data['gender'])
        self.assertEqual(self.profile.sports_you_can_play, data['sports_you_can_play'])
        self.assertEqual(self.profile.description, data['description'])
