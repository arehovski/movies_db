from django.db import models


# Create your models here.
class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='directors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)
    born_place = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='actors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    genres = [
        ("ан", "аниме"), ("би", "биография"), ("бо", "боевик"), ("ве", "вестерн"), ("во", "военный"),
        ("дт", "детектив"), ("де", "десткий"), ("дв", "для взрослых"), ("дк", "документальный"), ("др", "драма"),
        ("иг", "игра"), ("ис", "история"), ("ко", "комедия"), ("кн", "концерт"), ("км", "криминал"), ("мл", "мелодрама"),
        ("му", "музыка"), ("мф", "мультфильм"), ("мю", "мюзикл"), ("нв", "новости"), ("пр", "приключения"),
        ("тв", "реальное тв"), ("см", "семейный"), ("сп", "спорт"), ("тш", "ток-шоу"), ("тр", "триллер"),
        ("уж", "ужасы"), ("фн", "фантастика"), ("фэ", "фентези"), ("цр", "церемония")
    ]
    genre = models.CharField(max_length=50, choices=genres)

    def __str__(self):
        return f"{self.genre}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    country = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)
    duration_min = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='movies')
    premiere = models.DateField(null=True, blank=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
    is_tv_series = models.BooleanField()
    seasons_count = models.IntegerField(null=True, blank=True)
    series_count = models.IntegerField(null=True, blank=True)
    rating_kp = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=5)
    link_kp = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
