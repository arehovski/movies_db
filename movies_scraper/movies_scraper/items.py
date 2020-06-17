# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from movies.models import Director, Actor, Genre, Movie


class DirectorItem(DjangoItem):
    django_model = Director


class ActorItem(DjangoItem):
    django_model = Actor


class GenreItem(DjangoItem):
    django_model = Genre


class MovieItem(DjangoItem):
    django_model = Movie
