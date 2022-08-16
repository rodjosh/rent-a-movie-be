from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Movie, Rent
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication, JWTAuthentication])
def get_public_movies_api(request):

    rented_movies = Rent.objects.all()
    data_rented_ids = []

    for rented in rented_movies:
        data_rented_ids.append(rented.movie.id)

    movies = Movie.objects.exclude(id__in=data_rented_ids)
    data = []

    for movie in movies:
        data.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'img': movie.img
        })

    return Response({'status': 200, "movies": data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication, JWTAuthentication])
def get_movie_detail_api(request):
    keys = request.data.keys()
    if 'movieid' in keys:
        movies = Movie.objects.filter(id=request.data['movieid'])
        data = []
        for movie in movies:
            data.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description
            })
        return Response({'status': 200, "movie": data[0]})
    else:
        return Response({'status': 401, 'errors': ['movieid is required']})


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication, BasicAuthentication, JWTAuthentication])
def get_movies_api(request):
    movies = Movie.objects.all()
    data = []

    for movie in movies:
        data.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'img': movie.img
        })

    if request.method == 'POST':
        keys = request.data.keys()
        errors = []
        if 'title' not in keys:
            errors.append('title is required')
        if 'description' not in keys:
            errors.append('description is required')

        if len(errors) > 1:
            return Response({'created': False, "errors": errors})
        else:
            try:
                newmovie = Movie.objects.create(
                    title=request.data['title'], description=request.data['description'])
                newmovie.save()
            except Exception as e:
                return Response({'created': False, "errors": ['Network Error']})
            return Response({'created': True})

    if request.method == 'PATCH':
        keys = request.data.keys()
        errors = []
        if 'movieid' not in keys:
            errors.append('movieid is required')
        if 'title' not in keys:
            errors.append('title is required')
        if 'description' not in keys:
            errors.append('description is required')
        if len(errors) > 1:
            return Response({'updated': False, "errors": errors})
        else:
            try:
                movie = Movie.objects.get(id=request.data['movieid'])
                movie.title = request.data['title']
                movie.description = request.data['description']
                movie.save()

            except Exception as e:
                print(e)
                return Response({'updated': False, "errors": ['Network Error']})
            return Response({'updated': True})

    if request.method == 'DELETE':
        keys = request.data.keys()
        errors = []
        if 'movieid' not in keys:
            errors.append('movieid is required')

        if len(errors) > 1:
            return Response({'deleted': False, "errors": errors})
        else:
            try:
                movie = Movie.objects.get(id=request.data['movieid'])
                movie.delete()
            except Exception as e:
                return Response({'deleted': False, "errors": ['Network Error']})
            return Response({'deleted': True})

    return Response({'status': 200, "movies": data})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication, JWTAuthentication])
def rent_movies_api(request):
    if request.method == 'GET':
        return Response(
            {'rents': [{
                'id': x.movie.id,
                'title': x.movie.title,
                'description': x.movie.description,
                'img': x.movie.img
            } for x in Rent.objects.filter(user=request.user)]
                if len(Rent.objects.filter(user=request.user)) > 0
                else []})

    error = []
    keys = request.data.keys()
    if not 'movieid' in keys:
        error.append('movieid filed is required')

    if len(error) > 0:
        return Response({'errors': error, "rented": False})
    else:
        try:
            rent = Rent.objects.create(
                user=request.user,
                movie=Movie.objects.get(id=request.data['movieid'])
            )
            rent.save()
        except Exception as e:
            return Response({'rented': False, 'error': ['Network Issue']})

        return Response({"rented": True, "rent_details": {
            "rent_id": rent.id,
            'user_details': {
                "username": rent.user.username,
                "email": rent.user.email,
                "user_id": rent.user.id
            }, 'movie_details': {
                "title": rent.movie.title,
                "descrption": rent.movie.description,
                "movie_id": rent.movie.id
            }}})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, BasicAuthentication, JWTAuthentication])
def delete_rent_movies_api(request):
    error = []
    keys = request.data.keys()
    if not 'movieid' in keys:
        error.append('movieid filed is required')

    if len(error) > 0:
        return Response({'errors': error, "deleted": False})
    else:
        try:
            rent = Rent.objects.get(movie__id=request.data['movieid'])
            rent.delete()
        except Exception as e:
            return Response({'deleted': False, 'error': ['Network Issue']})

        return Response({"deleted": True})
