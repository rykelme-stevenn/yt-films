from django.contrib import admin

# Register your models here.

from .models import  Genre, Movie, Rating

# admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Rating)