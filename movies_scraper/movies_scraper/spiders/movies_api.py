# -*- coding: utf-8 -*-
import scrapy
import json

with open("/home/arehovski/PycharmProjects/movies_db/movie_ids_best.json", 'r') as f:
    movie_ids = json.load(f)


class MoviesApiSpider(scrapy.Spider):
    name = 'movies_api'
    movie_url = "https://kinopoiskapiunofficial.tech/api/v2.1/films"
    person_url = "https://kinopoiskapiunofficial.tech/api/v1/staff?filmId="

    def start_requests(self):
        for movie_id in movie_ids:
            yield scrapy.Request(f"{self.movie_url}/{movie_id}", meta={"movie_id": movie_id})

    def parse(self, response):
        print(response.url)

