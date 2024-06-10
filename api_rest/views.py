from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
# Create your views here.


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Movie, Genre, Rating
from django.contrib.auth.models import User
from .seralizer import UserSerializer, MovieSerializer, GenreSerializer, RatingSerializer
from cloudinary.uploader import upload
import json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_get(request):
  if(request.method == 'GET'):
    print(request.GET['email'])
    param_user = request.GET.get('user', None)
    param_email = request.GET.get('email', None)
    if(param_user): #se tiver um usuário específico no parametro da url
      try:
        user_id = request.GET['user'] #pegar o id do usuário na url
        user = User.objects.get(pk=user_id)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
      except:
        return Response(status=status.HTTP_404_NOT_FOUND)
      
    elif(param_email):
      try:
        email_param = request.GET['email'] #pegar o id do usuário na url
        user = User.objects.get(email=email_param)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
      except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
      users = User.objects.all() #traz todos os usuários

      serializer = UserSerializer(users, many=True)
      return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Erro ao buscar usuários'})


#Movie ===============================================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_create(request):
  if request.method == 'POST':

    if 'image' in request.FILES:
      image = request.FILES['image']
      result = upload(image)
      request.data['image'] = result['url']
    
    serializer = MovieSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def movie_permission(request):
  if request.method == 'PUT':
    try:
      movie_id = request.GET.get('movie')
      movie = Movie.objects.get(pk=movie_id)
      if(request.data['accept'] == True):
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
          serializer.save()
          return Response(status=status.HTTP_202_ACCEPTED)
      else:
        movie_id = request.GET.get('movie')
        movie = Movie.objects.get(pk=movie_id)
        movie.delete()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)  
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def movie_get(request):
  try:
    if(request.method == 'GET'):
      movies = Movie.objects.all()
      serializer = MovieSerializer(movies, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)  


#Genre ===============================================================================================

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def genre_create(request):
  print('a')
  try:
    if(request.method == 'POST'):
      new_genre = request.data
      serializer = GenreSerializer(data=new_genre)

      if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  except:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
  
@api_view(['GET'])
def only_genre_get(request):
  try:
    if(request.method == 'GET'):
      genres = Genre.objects.all()
      genre_data = GenreSerializer(genres, many=True).data
      return Response(genre_data, status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)


# Rating ===============================================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rating_get(request):
  if(request.method == 'GET'):
    try:
      user_id = request.GET.get('user')
      movie_id = request.GET.get('movie')
      rating = Rating.objects.get(movie_id=movie_id, user_id=user_id)
      rating_data = RatingSerializer(rating).data
      return Response({"rating": rating_data['rating']}, status=status.HTTP_200_OK)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND) 
  else: 
    return Response(status=status.HTTP_400_BAD_REQUEST)
  

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def rate(request):
  print('Received data:', request)
  
  if request.method == 'POST':
    new_rate = request.data
    serializer = RatingSerializer(data=new_rate)
    
    if serializer.is_valid():
      serializer.save()
      print("Saved rating:", serializer.data)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      print("Validation errors:", serializer.errors)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  if(request.method == 'PUT'):
    user_id = request.GET.get('user')
    movie_id = request.GET.get('movie')

    rating = Rating.objects.get(movie_id=movie_id, user_id=user_id)
    serializer = RatingSerializer(rating, data=request.data, partial=True)
    
    if serializer.is_valid():
      serializer.save()
      print("Saved rating:", serializer.data)
      return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
      print("Validation errors:", serializer.errors)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  else:
    return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
    