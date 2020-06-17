# -*- coding: utf-8 -*-
import scrapy
from movies_scraper.items import DirectorItem, ActorItem, GenreItem, MovieItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['www.kinopoisk.ru']
    start_urls = ['https://www.kinopoisk.ru/lists/top250/']

    def parse(self, response):
        item_link = response.xpath("//a[@class='selection-film-item-meta__link']/@href").get()
        abs_link = response.urljoin(item_link)
        yield scrapy.Request(abs_link, self.parse_movie)

    def parse_movie(self, response):
        movie = MovieItem()
        genre = GenreItem()
        genres = response.xpath("//span[@itemprop='genre']/a")
        for g in genres:
            genre["genre"] = g.xpath(".//text()").get()
        movie["title"] = response.xpath("//span[@class='moviename-title-wrapper']/text()").get()
        movie["year"] = int(response.xpath("(//td/div/a)[1]/text()").get())
        movie["country"] = response.xpath("(//td/div/a)[2]/text()").get()
        movie["duration_min"] = int(response.xpath("//td[@id='runtime']/text()").get().split()[0])
        movie["description"] = response.xpath("//div[@class='brand_words film-synopsys']/text()").get()
        movie["image"] = response.xpath("//div[@class='film-img-box feature_film_img_box feature_film_img_box_326']/a/img/@src").get()
        movie["premiere"] = response.xpath("//td[@id='div_world_prem_td2']/div/a[1]/text()").get()
        # movie["director"] =
        # movie["actors"] =
        movie["is_tv_series"] = False
        movie["rating_kp"] = float(response.xpath("//span[@class='rating_ball']/text()").get())
        movie["link_kp"] = response.url





