# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from movies.models import Director, Actor, Genre, Movie
import requests
from datetime import date
from movies_db.settings import BASE_DIR
import os


def format_date(date_str):
    date_str = date_str.split()
    months = [
        (1, "января"),
        (2, "февраля"),
        (3, "марта"),
        (4, "апреля"),
        (5, "мая"),
        (6, "июня"),
        (7, "июля"),
        (8, "августа"),
        (9, "сентября"),
        (10, "октября"),
        (11, "ноября"),
        (12, "декабря"),
    ]
    for month in months:
        if date_str[1] == month[1]:
            date_str[1] = date_str[1].replace(date_str[1], str(month[0]))
    try:
        form_date = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
    except TypeError:
        form_date = date(2000, 1, 1)
    return form_date


class MoviesScraperPipeline:
    def process_item(self, item, spider):
        director_item = item.get("director")
        try:
            director = Director.objects.filter(first_name=director_item["first_name"]).get(
                last_name=director_item["last_name"])
        except Director.DoesNotExist:
            image = requests.get(director_item.get("image"))
            image_path = os.path.join(
                BASE_DIR, f'media/directors/{director_item.get("first_name")}_{director_item.get("last_name")}.jpg')
            with open(image_path, "wb") as img:
                img.write(image.content)
            director = Director.objects.create(
                first_name=director_item.get("first_name"),
                last_name=director_item.get("last_name"),
                born_date=format_date(director_item.get("born_date")),
                born_place=director_item.get("born_place"),
                image=f'directors/{director_item.get("first_name")}_{director_item.get("last_name")}.jpg'
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
                image_path = os.path.join(
                    BASE_DIR, f'media/actors/{actor_item.get("first_name")}_{actor_item.get("last_name")}.jpg')
                with open(image_path, "wb") as img:
                    img.write(image.content)
                actor = Actor.objects.create(
                    first_name=actor_item.get("first_name"),
                    last_name=actor_item.get("last_name"),
                    born_date=format_date(actor_item.get("born_date")),
                    born_place=actor_item.get("born_place"),
                    image=f'directors/{actor_item.get("first_name")}_{actor_item.get("last_name")}.jpg'
                )
                actor.save()
            actors.append(actor)

        movie_item = item.get("movie")
        genre_items = item.get("genre")




        return item
