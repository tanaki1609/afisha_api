from collections import OrderedDict

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from films.serializers import FilmSerializer, MovieValidateSerializer
from films.models import Movie, Director, Genre
from films.serializers import DirectorSerializer, GenreSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class MovieListCreateAPIView(ListCreateAPIView):
    serializer_class = FilmSerializer
    queryset = Movie.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Get data from Serializer
        name = serializer.validated_data.get('name')  # None
        description = serializer.validated_data.get('description')  # None
        duration = serializer.validated_data.get('duration')
        is_active = serializer.validated_data.get('is_active')  # "Y"
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        # step 2: By this data create Movie
        movie = Movie.objects.create(
            name=name,
            description=description,
            duration=duration,
            is_active=is_active,
            director_id=director_id,
        )
        movie.genres.set(genres)
        movie.save()

        # step 3: Return right status and created data
        return Response(status=status.HTTP_201_CREATED, data={'movie_id': movie.id})


class GenreViewSet(ModelViewSet):  # GET->list, POST, GET->item, PUT, DELETE
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'




class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('results', data)
        ]))


class DirectorListCreateAPIView(ListCreateAPIView):  # GET, POST
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = CustomPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):  # GET, PUT, DELETE
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.prefetch_related('genres').get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error_message': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmSerializer(movie, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie.name = serializer.validated_data.get('name')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.is_active = serializer.validated_data.get('is_active')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.genres.set(serializer.validated_data.get('genres'))
        movie.save()
        return Response(status=status.HTTP_201_CREATED, data=FilmSerializer(movie).data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def movie_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect movies from DB
        movies = Movie.objects.select_related('director').prefetch_related('genres').all()

        # step 2: Reformat QuerySet to List of Dictionaries
        data = FilmSerializer(movies, many=True).data

        # step 3: Return response
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # step 0: Validation of data
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Get data from Serializer
        name = serializer.validated_data.get('name')  # None
        description = serializer.validated_data.get('description')  # None
        duration = serializer.validated_data.get('duration')
        is_active = serializer.validated_data.get('is_active')  # "Y"
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        # step 2: By this data create Movie
        movie = Movie.objects.create(
            name=name,
            description=description,
            duration=duration,
            is_active=is_active,
            director_id=director_id,
        )
        movie.genres.set(genres)
        movie.save()

        # step 3: Return right status and created data
        return Response(status=status.HTTP_201_CREATED, data={'movie_id': movie.id})
