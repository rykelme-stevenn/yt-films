# Models da aplicação api_rest

from django.db import models
import random


def upload_image(instance, filename):
    return f'{random.randint(0,100000)}/{filename}'

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Nickname {self.name} - Email {self.email} - id {self.id}'

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Name {self.name} - id {self.id}'    

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=100, default='')
    description = models.TextField()
    year = models.IntegerField()
    director = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    production = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Title {self.title} - Description {self.description} - id {self.id}'
    
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User: {self.user.name} - Movie: {self.movie.title} - Rating: {self.rating}'


# Create your models here.
