# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    access_key = "2105f22f98d48cf26c40ce23db1ec3bf"
    first_url = 'https://www.kinopoisk.ru/lists/top250/'
    params = {
        'access_key': access_key,
        'url': first_url
    }
    scrapestack = 'http://api.scrapestack.com/scrape'
    domain_to_scrape = "https://www.kinopoisk.ru"

    def start_requests(self):
        yield scrapy.Request(f'{self.scrapestack}?{urlencode(self.params)}',
                             callback=self.parse)

    def parse(self, response):
        item_link = response.xpath("//a[@class='selection-film-item-meta__link']/@href").get()
        abs_link = self.domain_to_scrape + item_link
        params = {
            'access_key': self.access_key,
            'url': abs_link
        }
        yield scrapy.Request(f"{self.scrapestack}?{urlencode(params)}", self.parse_movie)

    def parse_movie(self, response):
        genres = response.xpath("//span[@itemprop='genre']/a")
        genre = []
        for g in genres:
            genre.append(g.xpath(".//text()").get())
        title = response.xpath("//span[@class='moviename-title-wrapper']/text()").get()
        year = int(response.xpath("(//td/div/a)[1]/text()").get())
        countries = response.xpath("(//td/div)[2]/a")
        country = []
        for c in countries:
            country.append(c.xpath(".//text()").get())
        duration_min = int(response.xpath("//td[@id='runtime']/text()").get().split()[0])
        description = response.xpath("//div[@class='brand_words film-synopsys']/text()").get()
        image = response.xpath(
            "//div[@class='film-img-box feature_film_img_box feature_film_img_box_326']/a/img/@src").get()
        premiere = response.xpath("//td[@id='div_world_prem_td2']/div/a[1]/text()").get()
        is_tv_series = False
        rating_kp = float(response.xpath("//span[@class='rating_ball']/text()").get())
        link_kp = response.url
        director_url = self.domain_to_scrape + response.xpath("//td[@itemprop='director']/a/@href").get()
        params = {
            'access_key': self.access_key,
            'url': director_url
        }
        movie = {
            'title': title,
            'year': year,
            'country': country,
            'duration_min': duration_min,
            'description': description,
            'image': image,
            'premiere': premiere,
            'is_tv_series': is_tv_series,
            'rating_kp': rating_kp,
            'link_kp': link_kp,
            'genre': genre,
        }
        actors = response.xpath("//li[@itemprop='actors']/a")[:6]
        yield scrapy.Request(f"{self.scrapestack}?{urlencode(params)}", callback=self.parse_director,
                             meta={'movie': movie, 'actors': actors})

    def parse_director(self, response):
        movie = response.meta['movie']
        actors = response.meta['actors']
        director = self._get_person_data(response)
        actors_list = []
        actor_url = self.domain_to_scrape + actors.xpath(".//@href").get()
        params = {
            'access_key': self.access_key,
            'url': actor_url
        }
        yield scrapy.Request(f"{self.scrapestack}?{urlencode(params)}", callback=self.parse_actor,
                             meta={'movie': movie, 'director': director, "actors": actors, 'actors_list': actors_list})

    def parse_actor(self, response):
        movie = response.meta['movie']
        actors = response.meta['actors']
        director = response.meta['director']
        actors_list = response.meta['actors_list']
        actor = self._get_person_data(response)
        actors_list.append(actor)
        actors.pop(0)
        if not actors:
            yield {
                "movie": movie,
                "director": director,
                "actors": actors_list
            }
        else:
            actor_url = self.domain_to_scrape + actors.xpath(".//@href").get()
            params = {
                'access_key': self.access_key,
                'url': actor_url
            }
            yield scrapy.Request(f"{self.scrapestack}?{urlencode(params)}", callback=self.parse_actor,
                                 meta={'movie': movie, 'director': director, "actors": actors, 'actors_list': actors_list})

    def _get_person_data(self, response):
        first_name = response.xpath("//h1[@class='moviename-big']/text()").get().split()[0]
        last_name = " ".join(response.xpath("//h1[@class='moviename-big']/text()").get().split()[1:])
        born_date = " ".join(response.xpath("(//td[@class='birth'])[1]/a/text()").getall())
        born_place = " ".join(response.xpath("(//td[@class='birth'])[2]/span/a/text()").getall())
        image = response.xpath("//img[@itemprop='image']/@src").get()
        return {
            'first_name': first_name,
            'last_name': last_name,
            'born_date': born_date,
            'born_place': born_place,
            'image': image
        }
