from django.contrib.auth.models import AbstractUser
from django.db import models


class Quote(models.Model):
    quote = models.TextField()
    author = models.TextField()
    tags = models.TextField()

    def __str__(self):
        return self.quote


class Author(models.Model):
    fullname = models.TextField()
    born_date = models.DateField()
    born_location = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.fullname


class User(AbstractUser):
    username = models.CharField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username