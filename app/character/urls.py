from django.urls import path

from .views import list_character, list_character_quote, favorite_character, \
    favorite_quote_with_character, favorite_items


app_name = 'character'

urlpatterns = [
    path('characters/', list_character, name='characters'),
    path('characters/<character_id>/quotes',
         list_character_quote,
         name='character_quotes'
         ),
    path(
        'characters/<character_id>/favorites/',
        favorite_character,
        name='favorite_character'
    ),
    path(
        'characters/<character_id>/quotes/<quote_id>/favorites/',
        favorite_quote_with_character,
        name='favorite_quote_with_character'
    ),
    path('favorites/', favorite_items, name='favorites'),
]
