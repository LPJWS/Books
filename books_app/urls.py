from django.urls import include, path, re_path
from . import views

urlpatterns = [
  path('getbooks', views.get_books),
  path('getbooks/<int:book_id>', views.get_books),
  path('addbook', views.add_book),
  path('updatebook/<int:book_id>', views.update_book),
  path('deletebook/<int:book_id>', views.delete_book),

  path('getauthors', views.get_authors),
  path('getauthors/<int:author_id>', views.get_authors),
  path('addauthor', views.add_author),
  path('updateauthor/<int:author_id>', views.update_author),
  path('deleteauthor/<int:author_id>', views.delete_author),

  path('getgenres', views.get_genres),
  path('getgenres/<int:genre_id>', views.get_genres),
  path('addgenre', views.add_genre),
  path('updategenre/<int:genre_id>', views.update_genre),
  path('deletegenre/<int:genre_id>', views.delete_genre),
]
