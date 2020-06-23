# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from movies.models import Director, Actor, Genre, Country, Movie
import requests
from datetime import date, datetime
from movies_db.settings import BASE_DIR
import os
import logging


class MoviesScraperPipeline:
    def process_item(self, item, spider):
        director_item = item.get("director")
        try:
            director = Director.objects.filter(first_name=director_item["first_name"]).get(
                last_name=director_item["last_name"])
        except Director.DoesNotExist:
            image = requests.get(director_item.get("image"))
            rel_db_path = f'directors/{director_item.get("first_name")}_{director_item.get("last_name")}.jpg'
            image_path = os.path.join(BASE_DIR, f'media/{rel_db_path}')
            with open(image_path, "wb") as img:
                img.write(image.content)
            director = Director.objects.create(
                first_name=director_item.get("first_name"),
                last_name=director_item.get("last_name"),
                name_en=director_item.get("name_en"),
                born_date=self.get_data_from_string(director_item.get("born_date")),
                born_place=director_item.get("born_place"),
                image=rel_db_path,
                link=director_item.get("link")
            )
            director.save()

        actor_items = item.get("actors")
        actors = []
        for actor_item in actor_items:
            try:
                actor = Actor.objects.filter(first_name=actor_item["first_name"]).get(
                    last_name=actor_item["last_name"])
            except Actor.DoesNotExist:
                image = requests.get(actor_item.get("image"))
                rel_db_path = f'actors/{actor_item.get("first_name")}_{actor_item.get("last_name")}.jpg'
                image_path = os.path.join(BASE_DIR, f'media/{rel_db_path}')
                with open(image_path, "wb") as img:
                    img.write(image.content)
                actor = Actor.objects.create(
                    first_name=actor_item.get("first_name"),
                    last_name=actor_item.get("last_name"),
                    name_en=actor_item.get("name_en"),
                    born_date=self.get_data_from_string(actor_item.get("born_date")),
                    born_place=actor_item.get("born_place"),
                    image=rel_db_path,
                    link=actor_item.get("link")
                )
                actor.save()
            actors.append(actor)

        genre_items = item.get("movie").get("genre")
        genres = []
        for genre_item in genre_items:
            try:
                genre = Genre.objects.get(genre=genre_item)
            except Genre.DoesNotExist:
                genre = Genre.objects.create(
                    genre=genre_item
                )
            genres.append(genre)

        country_items = item.get("movie").get("country")
        countries = []
        for country_item in country_items:
            try:
                country = Country.objects.get(country=country_item)
            except Country.DoesNotExist:
                country = Country.objects.create(
                    country=country_item
                )
            countries.append(country)

        movie_item = item.get("movie")
        try:
            movie = Movie.objects.filter(year=movie_item.get("year")).get(title=movie_item.get("title"))
        except Movie.DoesNotExist:
            image = requests.get(movie_item.get("image"))
            rel_database_path = f"movies/{movie_item.get('title')}.jpg"
            image_path = os.path.join(BASE_DIR, f'media/{rel_database_path}')
            with open(image_path, "wb") as img:
                img.write(image.content)
            movie = Movie.objects.create(
                title=movie_item.get("title"),
                title_en=movie_item.get("title_en"),
                year=movie_item.get("year"),
                duration_min=self.format_duration(movie_item.get("duration_min")),
                description=movie_item.get("description"),
                image=rel_database_path,
                premiere=self.get_data_from_string(movie_item.get("premiere")),
                is_tv_series=movie_item.get("is_tv_series"),
                rating_imdb=movie_item.get("rating_imdb"),
                rating_kp=movie_item.get("rating_kp"),
                link_kp=movie_item.get("link_kp"),
                director=director,
            )
            movie.save()
            movie.genre.add(*genres)
            movie.country.add(*countries)
            movie.actors.add(*actors)
        else:
            logging.warning(f"The movie {movie.title} is already exists")
        return item

    @staticmethod
    def get_data_from_string(date_string):
        if date_string:
            return datetime.strptime(date_string, "%Y-%m-%d").date()

    @staticmethod
    def format_duration(time):
        if time:
            time = time.split(":")
            return (int(time[0]) * 60) + int(time[1])
        else:
            return 0
