from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
  path('user_get/', views.user_get, name="user_get"),
  path('movie_create/', views.movie_create, name="movie_create"),
  path('movie_get/', views.movie_get, name="movie_get"),
  path('movie_permission/', views.movie_permission, name="movie_permission"),
  path('genre_create/', views.genre_create, name="genre_create"),
  path('genre_get/', views.genre_get, name="genre_get"),
  path('only_genre_get/', views.only_genre_get, name="only_genre_get"),
  path('rating_get/', views.rating_get, name="rating_get"),
  path('rate/', views.rate, name="rate")
]