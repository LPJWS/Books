from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Author, Book, Genre


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'img',
            'published_date',
            'author',
            'genre'
        ]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'img',
            'birth_date'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name'
        ]
