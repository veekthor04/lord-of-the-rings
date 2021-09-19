from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class CustomUser(AbstractUser):
    """Custom user model"""
    email = models.EmailField(unique=True)


class Favorite(models.Model):
    """User's favorite items"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    character = ArrayField(
        models.CharField(max_length=30, null=True), blank=True,
        default=list
    )
    quote = ArrayField(
        models.CharField(max_length=30, null=True),
        blank=True, default=list
    )

    def __str__(self):
        return self.user.username
