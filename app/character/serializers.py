from rest_framework import serializers

from core.models import Character, Quote


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for character objects"""

    class Meta:
        model = Character
        exclude = ('liked_by', )


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for quote objects"""

    class Meta:
        model = Quote
        exclude = ('liked_by',)


class FavoriteSerializer(serializers.Serializer):
    """Serializer for character and quote"""
    character = CharacterSerializer(read_only=True, many=True)
    quote = QuoteSerializer(read_only=True, many=True)
