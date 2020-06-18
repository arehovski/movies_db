# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from movies.models import Director, Actor, Genre, Movie
from .items import DirectorItem, ActorItem, GenreItem, MovieItem
import logging


class MoviesScraperPipeline:
    def process_item(self, item, spider):
        return item
