from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


# Reverse URLs
CHARACTER_URL = reverse('character:characters')


# Helper function to create user
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Unauthenticated user request
class PublicUserApiTests(TestCase):
    """Test the character public API"""

    def setUp(self):
        self.client = APIClient()

    def test_character_endpoint(self):
        """test"""
        response = self.client.get(CHARACTER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Authenticated user request
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            username='testuser',
            email='test@test.com',
            password='Testpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
