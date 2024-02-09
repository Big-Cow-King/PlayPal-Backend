from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile


class ProfileTestCase(APITestCase):
    def setUp(self):
        # Create a user and associated profile for testing
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        Profile.objects.create(user=self.user, phone_no='1234567890', name='Test User', gender='Male', age=25,
                               description='Original description', sports_you_can_play='Tennis')

        # URL for getting the profile and editing the profile
        self.get_profile_url = reverse('profile_view')  # Corrected URL name
        self.edit_profile_url = reverse('edit_profile')  # Corrected URL name

        # Log in the user
        self.client.login(username='testuser', password='testpassword123')

    def test_retrieve_profile(self):
        # Attempt to retrieve the profile
        response = self.client.get(self.get_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_no'], '1234567890')
        self.assertEqual(response.data['name'], 'Test User')

    def test_update_profile(self):
        # Data to update the profile
        data = {
            'name': 'Updated Name',
            'phone_no': '0987654321',
            'gender': 'Female',
            'age': 30,
            'description': 'Updated description',
            'sports_you_can_play': 'Soccer, Tennis',
            'email_product': True
        }

        # Attempt to update the profile
        response = self.client.post(self.edit_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refetch the profile to verify updates
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.name, 'Updated Name')
        self.assertEqual(self.user.profile.phone_no, '0987654321')


