# -*- coding: utf-8 -*-
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['www.kinopoisk.ru']
    start_urls = ['https://www.kinopoisk.ru/lists/top250/']

    def parse(self, response):
        item_link = response.xpath("//a[@class='selection-film-item-meta__link']/@href").get()
        abs_link = response.urljoin(item_link)
        yield scrapy.Request(abs_link, self.parse_movie)

    def parse_movie(self, response):
        genres = response.xpath("//span[@itemprop='genre']/a")
        genre = []
        for g in genres:
            genre.append(g.xpath(".//text()").get())
        title = response.xpath("//span[@class='moviename-title-wrapper']/text()").get()
        year = int(response.xpath("(//td/div/a)[1]/text()").get())
        country = response.xpath("(//td/div/a)[2]/text()").get()
        duration_min = int(response.xpath("//td[@id='runtime']/text()").get().split()[0])
        description = response.xpath("//div[@class='brand_words film-synopsys']/text()").get()
        image = response.xpath("//div[@class='film-img-box feature_film_img_box feature_film_img_box_326']/a/img/@src").get()
        premiere = response.xpath("//td[@id='div_world_prem_td2']/div/a[1]/text()").get()
        is_tv_series = False
        rating_kp = float(response.xpath("//span[@class='rating_ball']/text()").get())
        link_kp = response.url
        director_url = response.urljoin(response.xpath("//td[@itemprop='director']/a/@href").get())

        def parse_director():
            yield scrapy.Request(director_url, callback=self.parse_person)

        def parse_actor():
            for actor in response.xpath("//li[@itemprop='actors']/a")[:6]:
                yield scrapy.Request(response.urljoin(actor.xpath(".//@href").get()), callback=self.parse_person)
        yield {
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
            'director': parse_director(),
            'actors': parse_actor()
        }


    def parse_person(self, response):
        first_name = response.xpath("//h1[@class='moviename-big']/text()").get().split()[0]
        last_name = " ".join(response.xpath("//h1[@class='moviename-big']/text()").get().split()[1:])
        born_date = " ".join(response.xpath("(//td[@class='birth'])[1]/a/text()").getall())
        born_place = " ".join(response.xpath("(//td[@class='birth'])[2]/span/a/text()").getall())
        image = response.xpath("//img[@itemprop='image']/@src").get()
        yield {
            'first_name': first_name,
            'last_name': last_name,
            'born_date': born_date,
            'born_place': born_place,
            'image': image
        }


