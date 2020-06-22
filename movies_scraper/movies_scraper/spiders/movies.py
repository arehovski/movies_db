# -*- coding: utf-8 -*-
import scrapy
from scraper_api import ScraperAPIClient


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    client = ScraperAPIClient("045eef96d928d59be026b8aafb655f94")
    domain_to_scrape = "https://www.kinopoisk.ru"

    def start_requests(self):
        yield scrapy.Request(self.client.scrapyGet("https://www.kinopoisk.ru/lists/top250/"),
                             callback=self.parse)

    def parse(self, response):
        page_movies = response.xpath("//a[@class='selection-film-item-meta__link']")
        for movie in page_movies:
            movie_link = self.domain_to_scrape + movie.xpath(".//@href").get()
            yield scrapy.Request(self.client.scrapyGet(movie_link), self.parse_movie, meta={"movie_link": movie_link})
        for i in range(2, 10):
            next_page = self.domain_to_scrape + f"/lists/top250/?page={i}&tab=all"
            yield scrapy.Request(self.client.scrapyGet(next_page), callback=self.parse)

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
        image = response.xpath("//a[@class='popupBigImage']/img/@src").get()
        premiere = response.xpath("//td[@id='div_world_prem_td2']/div/a[1]/text()").get()
        is_tv_series = False
        rating_kp = float(response.xpath("//span[@class='rating_ball']/text()").get())
        link_kp = response.meta["movie_link"]
        director_url = self.domain_to_scrape + response.xpath("//td[@itemprop='director']/a/@href").get()
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
        yield scrapy.Request(self.client.scrapyGet(director_url), callback=self.parse_director,
                             meta={'movie': movie, 'actors': actors})

    def parse_director(self, response):
        movie = response.meta['movie']
        actors = response.meta['actors']
        director = self._get_person_data(response)
        actors_list = []
        actor_url = self.domain_to_scrape + actors.xpath(".//@href").get()
        yield scrapy.Request(self.client.scrapyGet(actor_url), callback=self.parse_actor,
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
            yield scrapy.Request(self.client.scrapyGet(actor_url), callback=self.parse_actor,
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
