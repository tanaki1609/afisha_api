from rest_framework import serializers
from films.models import Movie, Director, Genre
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'first_name last_name birthday age'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    # genres = GenreSerializer(many=True)
    genre_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', 'created', 'director', 'genres', 'genre_list',
                  'genre_str']
        # fields = '__all__'
        # exclude = ['id', 'name']
        depth = 1

    def get_genre_list(self, movie):
        return [i.name for i in movie.genres.all()]


class MovieValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, min_length=2)
    description = serializers.CharField(required=False)
    duration = serializers.IntegerField(min_value=5, max_value=300)
    is_active = serializers.BooleanField()
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField(min_value=1))

    # def validate(self, attrs):
    #     id = attrs['director_id']
    #     try:
    #         Director.objects.get(id=id)
    #     except Director.DoesNotExist:
    #         raise ValidationError(f'Director with id ({id}) does not exist!')
    #     return attrs

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError(f'Director with id ({director_id}) does not exist!')
        return director_id

    def validate_genres(self, genres):  # [1,2,100]
        genres_from_db = Genre.objects.filter(id__in=genres)
        if len(genres_from_db) != len(genres):
            raise ValidationError("Genre does not exist!")
        return genres
