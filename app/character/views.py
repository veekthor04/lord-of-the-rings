import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, \
    ConnectionError

from decouple import config

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.models import Favorite


# Constants
THE_ONE_API_TOKEN = config('THE_ONE_API_TOKEN')
HEADERS = {"Authorization": "Bearer " + THE_ONE_API_TOKEN}
THE_ONE_API_BASE_URL = config('THE_ONE_API_BASE_URL')


# Create your views here.
@swagger_auto_schema(
    method='get',
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )},
)
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
            status=status.HTTP_503_SERVICE_UNAVAILABLE
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


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )},
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
            status=status.HTTP_503_SERVICE_UNAVAILABLE
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


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_character(request, character_id):
    """Adds character to a user's favorite character list"""

    # Get users favorite object
    user_favorite = Favorite.objects.get_or_create(
        user=request.user
    )

    # Check if character does not exist the adds
    if user_favorite[0].character.count(character_id) < 1:

        user_favorite[0].character.append(character_id)
        user_favorite[0].save()

    return Response(
        {"message": "character has been added to user's favorite"},
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_quote_with_character(request, character_id, quote_id):
    """Adds quote and character to a user's favorite quote and
    character list"""

    # Get users favorite object
    user_favorite = Favorite.objects.get_or_create(
        user=request.user
    )

    # Check if character does not exist then adds
    if user_favorite[0].character.count(character_id) < 1:

        user_favorite[0].character.append(character_id)

        # Check if quote does not exist then adds
    if user_favorite[0].quote.count(quote_id) < 1:

        user_favorite[0].quote.append(quote_id)

    user_favorite[0].save()

    return Response(
        {"message": "character and quote has been added to user's favorite"},
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'character': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description='A list of characters'
            ),
            'quote': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description='A list of quotes'
            ),
        }
    )}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_items(request):
    """Returns a list of user's favorite items"""

    user_favorite = Favorite.objects.filter(user=request.user)

    if user_favorite.exists():

        character_query = ','.join(user_favorite.first().character)
        quote_query = ','.join(user_favorite.first().quote)

    try:
        character_response = requests.get(
            THE_ONE_API_BASE_URL + "/character",
            headers=HEADERS,
            timeout=5,
            params={
                '_id': character_query
            }
        )

        quote_response = requests.get(
            THE_ONE_API_BASE_URL + "/quote",
            headers=HEADERS,
            timeout=5,
            params={
                '_id': quote_query
            }
        )
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):

        # Server error
        return Response(
            {"error": "service is unavailable, try again"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    else:

        # Success response
        if character_response.status_code == 200 and \
                quote_response.status_code == 200:

            character_data = character_response.json()
            quote_data = quote_response.json()
            return Response({
                'character': character_data['docs'],
                'quote': quote_data['docs']
            }, status=status.HTTP_200_OK)

    return Response({
        'message': 'not found'
    }, status=status.HTTP_404_NOT_FOUND)
