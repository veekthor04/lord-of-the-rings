import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, \
    ConnectionError

from decouple import config

from django.utils.decorators import method_decorator

from rest_framework import status, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.models import Character, Quote
from .serializers import CharacterSerializer, QuoteSerializer, \
    FavoriteSerializer


# Constants
THE_ONE_API_TOKEN = config('THE_ONE_API_TOKEN')
HEADERS = {"Authorization": "Bearer " + THE_ONE_API_TOKEN}
THE_ONE_API_BASE_URL = config('THE_ONE_API_BASE_URL')


# Create your views here.
@api_view(['GET'])
def list_character(request):
    """Retrieves character from the-one-api and returns it"""
    try:
        response = requests.get(
            THE_ONE_API_BASE_URL + "/character",
            headers=HEADERS,
            timeout=5
        )
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):

        # Server error
        return Response(
            {"error": "service is unavailable, try again"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:

        # Success response
        if response.status_code == 200:

            data = response.json()
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Request failed"},
            status=response.status_code
        )


@api_view(['GET'])
def list_character_quote(request, character_id):
    """Retrieves character's quote from the-one-api and returns it"""

    try:

        response = requests.get(
            THE_ONE_API_BASE_URL + "/character/" + character_id + '/quote',
            headers=HEADERS,
            timeout=5
        )
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):

        # Server error
        return Response(
            {"error": "service is unavailable, try again"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:

        # Success response
        if response.status_code == 200:

            data = response.json()
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Request failed"},
            status=response.status_code
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_character(request, character_id):
    """Adds character to a user's favorite character list"""

    try:

        # Check if character exist
        response = requests.get(
            THE_ONE_API_BASE_URL + "/character/" + character_id,
            headers=HEADERS,
            timeout=5
        )
        # Success response
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):

        # Server error
        return Response(
            {"error": "service is unavailable, try again"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:

        # Success response
        if response.status_code == 200:

            # Checks if an item was returned
            if response.json()['docs']:

                # Create character object in db and add user.
                Character.objects.get_or_create(
                    **response.json()['docs'][0]
                )[0].liked_by.add(request.user)

                return Response(
                    {"message": "character has been added"},
                    status=status.HTTP_201_CREATED
                )

        # Character not found or invalid response
        return Response(
            {"error": "character not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_quote_with_character(request, character_id, quote_id):
    """Adds quote and character to a user's favorite quote and
    character list"""

    # Check if quote for the given character exist
    try:
        response = requests.get(
            THE_ONE_API_BASE_URL + '/quote',
            headers=HEADERS,
            params={
                'character': character_id,
                '_id': quote_id
            },
            timeout=5
        )
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):

        # Server error
        return Response(
            {"error": "service is unavailable, try again"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:

        # Success response
        if response.status_code == 200:

            # Checks if an item was returned
            if response.json()['docs']:

                # Create character object in db and add user.
                character = Character.objects.filter(pk=character_id).first()
                if not character:
                    response_2 = requests.get(
                        THE_ONE_API_BASE_URL + "/character/" + character_id,
                        headers=HEADERS,
                        timeout=5
                    )
                    character = Character.objects.get_or_create(
                        **response_2.json()['docs'][0]
                    )[0]
                    character.liked_by.add(request.user)

                # Create quote id in db and adds user.
                dialog = response.json()['docs'][0]['dialog']
                movie = response.json()['docs'][0]['movie']
                _id = response.json()['docs'][0]['_id']
                Quote.objects.get_or_create(
                    character=character,
                    _id=_id,
                    dialog=dialog,
                    movie=movie
                )[0].liked_by.add(request.user)
                return Response(
                    {"message": "character has been added"},
                    status=status.HTTP_201_CREATED
                )

        return Response(
            {"error": "character with quote not found"},
            status=status.HTTP_404_NOT_FOUND
        )


class MyLikedCharacters(generics.ListAPIView):
    """Returns a user's favorite character list"""
    serializer_class = CharacterSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Filters character and by logged in user"""
        return Character.objects.filter(liked_by=self.request.user)


class MyLikedQuotes(generics.ListAPIView):
    """Returns a user's favorite quote list"""
    serializer_class = QuoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Filters quote and by logged in user"""
        return Quote.objects.filter(liked_by=self.request.user)



class FavoriteView(views.APIView):
    """Returns a list of user's favorite items"""
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={200: FavoriteSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        favorites = {}
        favorites['character'] = Character.objects.filter(liked_by=self.request.user)
        favorites['quote'] = Quote.objects.filter(liked_by=self.request.user)
        serializer = FavoriteSerializer(favorites)
        return Response(serializer.data, status=status.HTTP_200_OK)
