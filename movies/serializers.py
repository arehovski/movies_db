from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['first_name', 'last_name', 'name_en', 'born_date', 'born_place', 'link']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['first_name', 'last_name', 'name_en', 'born_date', 'born_place', 'link']


class MovieSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)
    director = DirectorSerializer()
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'title_en', 'year', 'country', 'genre', 'duration_min', 'description', 'premiere',
            'director', 'actors', 'is_tv_series', 'rating_imdb', 'rating_kp', 'link_kp'
        ]
