from django.shortcuts import render
from django import views
from .models import Actor, Director, Movie, Genre, Country
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


def pagination(iterable, request):
    paginator = Paginator(iterable, 15)
    page = request.GET.get('page')
    try:
        iterable = paginator.page(page)
    except PageNotAnInteger:
        iterable = paginator.page(1)
    except EmptyPage:
        iterable = paginator.page(paginator.num_pages)
    return iterable


# Create your views here.
class HomePage(views.View):
    movies = Movie.objects.all()
    template = "base.html"

    def get(self, request):
        self.movies = pagination(self.movies, request)
        context = {
            'movies': self.movies,
        }
        return render(request, self.template, context)


class GenreView(views.View):
    template = "base.html"

    def get(self, request, genre):
        movies = Movie.objects.filter(genre__genre=f"{genre}")
        movies = pagination(movies, request)
        return render(request, self.template, context={'movies': movies})


class YearView(views.View):
    def get(self, request, year):
        movies = Movie.objects.filter(year=int(f"{year}"))
        movies = pagination(movies, request)
        return render(request, "base.html", context={'movies': movies})


class CountryView(views.View):
    def get(self, request, country):
        movies = Movie.objects.filter(country__country__exact=f"{country}")
        movies = pagination(movies, request)
        return render(request, "base.html", context={'movies': movies})


class MovieView(views.View):
    template = 'movie.html'

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        similar_movies = Movie.objects.filter(genre__genre=movie.genre.all()[0]).exclude(pk=movie.pk)[:8]
        context = {
            'movie': movie,
            'similar_movies': similar_movies
        }
        return render(request, self.template, context=context)
