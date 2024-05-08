from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
  # path('get_users', views.get_users, name="get_all_users"),
  # path('get_user/<str:id>', views.get_user, name="get_user"),
  path('user_manager/', views.user_manager, name="user_manager"),
  path('movie_create/', views.movie_create, name="movie_create"),
  path('movie_get/', views.movie_get, name="movie_get"),
  path('genre_create/', views.genre_create, name="genre_create"),
  path('genre_get/', views.genre_get, name="genre_get"),
  path('rating/', views.rating, name="rating")
]