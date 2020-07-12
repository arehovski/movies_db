# -*- coding: utf-8 -*-
import scrapy
import json

with open("/root/movies_db/movie_ids_best.json", 'r') as f:
    movie_ids = json.load(f)


class MoviesApiSpider(scrapy.Spider):
    name = 'movies_api'
    person_url = "https://kinopoiskapiunofficial.tech/api/v1/staff?filmId="

    @staticmethod
    def _get_movie_url(film_id):
        return f"https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}?append_to_response=RATING"

    def start_requests(self):
        for movie_id in movie_ids:
            yield scrapy.Request(self._get_movie_url(movie_id), callback=self.parse, meta={'movie_id': movie_id})

    def parse(self, response):
        json_response = json.loads(response.text)
        data = json_response.get("data")
        genres = data.get("genres")
        genre = []
        for g in genres:
            genre.append(g.get("genre"))
        title = data.get("nameRu")
        title_en = data.get("nameEn")
        year = int(data.get("year")[:4])
        countries = data.get("countries")
        country = []
        for c in countries:
            country.append(c.get("country"))
        duration_min = data.get("filmLength")
        description = data.get("description")
        image = data.get("posterUrl")
        premiere = data.get("premiereWorld")
        if data.get("type") == "TV_SHOW":
            is_tv_series = True
        else:
            is_tv_series = False
        rating_imdb = float(json_response.get("rating").get("ratingImdb"))
        rating_kp = float(json_response.get("rating").get("rating"))
        link_kp = data.get("webUrl")
        movie = {
            'title': title,
            'title_en': title_en,
            'year': year,
            'country': country,
            'duration_min': duration_min,
            'description': description,
            'image': image,
            'premiere': premiere,
            'is_tv_series': is_tv_series,
            "rating_imdb": rating_imdb,
            'rating_kp': rating_kp,
            'link_kp': link_kp,
            'genre': genre,
        }
        movie_id = response.meta["movie_id"]
        yield scrapy.Request(self.person_url+str(movie_id), callback=self.parse_person, meta={"movie": movie})

    def parse_person(self, response):
        movie = response.meta["movie"]
        json_response = json.loads(response.text)
        director = self._get_person_data(json_response[0])
        actors = []
        for person in json_response[1:]:
            if person.get("professionKey") == "ACTOR":
                actor = self._get_person_data(person)
                actors.append(actor)
                if len(actors) >= 7:
                    break
        yield {
            'movie': movie,
            'director': director,
            'actors': actors
        }

    @staticmethod
    def _get_person_data(person):
        first_name = person.get("nameRu").split()[0]
        last_name = " ".join(person.get("nameRu").split()[1:])
        name_en = person.get("nameEn")
        link = f"https://www.kinopoisk.ru/name/{person.get('staffId')}"
        image = person.get("posterUrl")
        return {
            'first_name': first_name,
            'last_name': last_name,
            'name_en': name_en,
            'link': link,
            'image': image
        }

