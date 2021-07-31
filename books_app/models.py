from django.db import models

import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    img = models.ImageField(upload_to='books/')
    published_date = models.DateField(blank=True, null=True)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s "%s"' % (self.author.name, self.title)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='authors/')
    birth_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
