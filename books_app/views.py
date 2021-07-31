from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookSerializer, AuthorSerializer, GenreSerializer
from .models import Book, Author, Genre
from rest_framework import status

import json
from django.core.exceptions import ObjectDoesNotExist

import base64
from django.core.files.base import ContentFile
from transliterate import translit


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_book(request):
    payload = json.loads(request.body)
    try:
        author = Author.objects.get(id=payload["author"])
        genre = Genre.objects.get(id=payload["genre"])

        # Base64 image upload
        # fmt, imgstr = payload["img"].split(';base64,')
        # ext = fmt.split('/')[-1]
        # filename = translit(payload["title"], reversed=True).replace(' ', '_').lower()
        # img_data = ContentFile(base64.b64decode(imgstr), name='%s.%s' % (filename, ext))

        book = Book.objects.create(
            title=payload["title"],
            description=payload["description"],
            author=author,
            # img=img_data,
            img=payload["img"],
            published_date=payload["published_date"],
            genre=genre
        )
        serializer = BookSerializer(book)
        return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_book(request, book_id):
    payload = json.loads(request.body)
    try:
        book_item = Book.objects.filter(id=book_id)
        book_item.update(**payload)
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return JsonResponse({'book': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_authors(request):
    books = Author.objects.all()
    serializer = AuthorSerializer(books, many=True)
    return JsonResponse({'authors': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_author(request):
    payload = json.loads(request.body)

    # Base64 image upload
    # fmt, imgstr = payload["img"].split(';base64,')
    # ext = fmt.split('/')[-1]
    # filename = translit(payload["name"], reversed=True).replace(' ', '_').lower()
    # img_data = ContentFile(base64.b64decode(imgstr), name='%s.%s' % (filename, ext))

    try:
        author = Author.objects.create(
            name=payload["name"],
            # img=img_data,
            img=payload["img"],
            birth_date=payload["birth_date"]
        )
        serializer = AuthorSerializer(author)
        return JsonResponse({'authors': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_author(request, author_id):
    payload = json.loads(request.body)
    try:
        author_item = Author.objects.filter(id=author_id)
        author_item.update(**payload)
        author = Author.objects.get(id=author_id)
        serializer = AuthorSerializer(author)
        return JsonResponse({'author': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_genres(request):
    user = request.user
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return JsonResponse({'genres': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_genre(request):
    payload = json.loads(request.body)
    try:
        genre = Genre.objects.create(
            name=payload["name"],
        )
        serializer = GenreSerializer(genre)
        return JsonResponse({'genre': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_genre(request, genre_id):
    payload = json.loads(request.body)
    try:
        genre_item = Genre.objects.filter(id=genre_id)
        genre_item.update(**payload)
        genre = Genre.objects.get(id=genre_id)
        serializer = GenreSerializer(genre)
        return JsonResponse({'genre': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_genre(request, genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
