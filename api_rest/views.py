from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User, Movie, Genre, Rating
from .seralizer import UserSerializer, MovieSerializer, GenreSerializer, RatingSerializer

import json

# @api_view(['GET'])
# def get_users(request):
#   if(request.method == 'GET'):
#     users = User.objects.all() #traz todos os usuários

#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
#   return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Erro ao buscar usuários'})

# @api_view(['GET'])
# def get_user(request, id):
#   if(request.method == 'GET'):
#     try:
#       user = User.objects.get(pk=id) #traz um usuário específico de acordo com o id(pk=primary key)
#       serializer = UserSerializer(user, many=False)
#       return Response(serializer.data)
#     except:
#       return Response(status=status.HTTP_404_NOT_FOUND)
#   return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def user_manager(request):
  print(request.method)
  if(request.method == 'GET'):
    try: 
      if(request.GET['user']): #se tiver um usuário específico no parametro da url
        try:
          user_id = request.GET['user'] #pegar o id do usuário na url
          user = User.objects.get(pk=user_id)

          serializer = UserSerializer(user, many=False)
          return Response(serializer.data, status=status.HTTP_200_OK)
        except:
          return Response(status=status.HTTP_404_NOT_FOUND)
      else:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True) 
        return (serializer.data)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
  if(request.method == 'POST'):
    new_user = request.data
    serializer = UserSerializer(data=new_user)

    if(serializer.is_valid()): #Verifica se os dados que estão sendo passados são válidos
      serializer.save() #Salva os dados no banco de dados
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if(request.method == 'PUT'):
    try:
      user_id = request.GET['user']
      update_user = User.objects.get(pk=user_id)
      
      serializer = UserSerializer(update_user, data=request.data)

      if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
  if(request.method == 'DELETE'):
    try:
      user_id = request.GET['user']
      user = User.objects.get(pk=user_id)
      user.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)





#Movie

@api_view(['POST'])
def movie_create(request):
  if request.method == 'POST':
    serializer = MovieSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def movie_get(request):
  try:
    if(request.method == 'GET'):
      movies = Movie.objects.all()
      serializer = MovieSerializer(movies, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)  



#Genre

@api_view(['POST', 'GET'])
def genre_create(request):
  try:
    if(request.method == 'POST'):
      new_genre = request.data
      serializer = GenreSerializer(data=new_genre)

      if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def genre_get(request):
  try:
    if(request.method == 'GET'):
      genres = Genre.objects.all()
      genre_data = GenreSerializer(genres, many=True).data

      for genre in genre_data:
        movies = Movie.objects.filter(genre=genre['id'])
        movie_data = MovieSerializer(movies, many=True).data
        genre['movies'] = movie_data

      return Response(genre_data, status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
@api_view(['GET', 'POST', 'PUT'])
def rating(request):
  if(request.method == 'GET'):
    try:
      user_id = request.GET.get('user')
      movie_id = request.GET.get('movie')
      rating = Rating.objects.get(movie_id=movie_id, user_id=user_id)
      rating_data = RatingSerializer(rating).data
      return Response({"rating": rating_data['rating']}, status=status.HTTP_200_OK)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND) 

  elif(request.method == 'POST'):
    try:
      new_rate = request.data
      serializer = RatingSerializer(data=new_rate)
      if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  elif(request.method == 'PUT'):
    try:
      user_id = request.GET.get('user')
      movie_id = request.GET.get('movie')
      new_rate = request.data
      update_rating = Rating.objects.get(movie_id=movie_id, user_id=user_id)
      
      serializer = RatingSerializer(update_rating, data=new_rate)
      # serializer = RatingSerializer(data=new_rate)
      if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  else: 
    return Response(status=status.HTTP_400_BAD_REQUEST)