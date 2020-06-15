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


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    country = models.CharField(max_length=255)
    genre = models.CharField(max_length=1000)
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
