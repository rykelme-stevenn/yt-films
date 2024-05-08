# Transformar o retorno em json para o frontend

from rest_framework import serializers
from .models import User, Movie, Genre, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'name', 'email', 'password', 'created_at', 'updated_at']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        # fields = ['id', 'name', 'created_at', 'updated_at']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'year', 'director', 'poster', 'link', 'production', 'genre', 'created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'