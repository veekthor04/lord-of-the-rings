from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


# Reverse URLs
CHARACTER_URL = reverse('character:characters')
FAVORITE_URL = reverse('character:favorites')


# Helper function to create user
def create_user(**params):
    return get_user_model().objects.create_user(**params)


def favorite_character_url(character_id):
    """Return fovorite character URL with character_id"""
    return reverse('character:favorite_character', args=[character_id])


def favorite_quote_with_character_url(character_id, quote_id):
    """Return favorite quote with character URL with character_id and
    quote_id"""
    return reverse(
        'character:favorite_quote_with_character',
        args=[character_id, quote_id]
    )


# Unauthenticated user request
class PublicUserApiTests(TestCase):
    """Test the character public API"""

    def setUp(self):
        self.client = APIClient()

    def test_character_endpoint(self):
        """test"""
        response = self.client.get(CHARACTER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_required_for_favorite_character(self):
        """Test that authentication is required for favorite_character"""
        character_id = "testid"

        url = favorite_character_url(character_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_favorite_quote_with_character(self):
        """Test that authentication is required for favorite quote
        with character"""
        character_id = "test_character_id"
        quote_id = "test_quote_id"

        url = favorite_quote_with_character_url(character_id, quote_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_favorites(self):
        """Test that authentication is required for favorites"""

        response = self.client.get(FAVORITE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_favorite_character_success(self):
        """Test that fovorite character is successful"""

        character_id = "testid"

        url = favorite_character_url(character_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favorite_quote_with_character_success(self):
        """Test that fovorite character is successful"""

        character_id = "test_character_id"
        quote_id = "test_quote_id"

        url = favorite_quote_with_character_url(character_id, quote_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
