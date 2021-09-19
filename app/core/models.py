from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model"""
    email = models.EmailField(unique=True)


class Character(models.Model):
    """User's favorite characters"""
    _id = models.CharField(max_length=30, primary_key=True, unique=True)
    height = models.CharField(max_length=50, blank=True)
    race = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    birth = models.CharField(max_length=50, blank=True)
    spouse = models.CharField(max_length=50, blank=True)
    death = models.CharField(max_length=50, blank=True)
    realm = models.CharField(max_length=50, blank=True)
    hair = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    wikiUrl = models.URLField(max_length=200, blank=True)
    liked_by = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self._id


class Quote(models.Model):
    """User's favorite quote"""
    _id = models.CharField(max_length=30, primary_key=True, unique=True)
    dialog = models.TextField()
    movie = models.CharField(max_length=30)
    character = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='quote'
    )
    liked_by = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self._id
