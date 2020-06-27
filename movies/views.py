from django.shortcuts import render
from django import views
from .models import Actor, Director, Movie, Genre, Country
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


def pagination(objects_list, request):
    paginator = Paginator(objects_list, 15)
    page = request.GET.get('page')
    try:
        objects_list = paginator.page(page)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        objects_list = paginator.page(paginator.num_pages)
    return objects_list


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

    @staticmethod
    def get_movies(query_param):
        return Movie.objects.filter(genre__genre=query_param)

    def get(self, request, param):
        movies = self.get_movies(param)
        movies = pagination(movies, request)
        return render(request, self.template, context={'movies': movies})


class YearView(GenreView):
    @staticmethod
    def get_movies(query_param):
        return Movie.objects.filter(year=query_param)


class CountryView(GenreView):
    @staticmethod
    def get_movies(query_param):
        return Movie.objects.filter(country__country__exact=query_param)


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


class DirectorView(views.View):
    template = 'director.html'
    model = Director

    @staticmethod
    def get_related_movies(query_param):
        return Movie.objects.filter(director=query_param)

    def get(self, request, pk):
        person = get_object_or_404(self.model, pk=pk)
        related_movies = self.get_related_movies(person.id)
        context = {
            'person': person,
            'related_movies': related_movies
        }
        return render(request, self.template, context)


class ActorView(DirectorView):
    template = 'actor.html'
    model = Actor

    @staticmethod
    def get_related_movies(query_param):
        return Movie.objects.filter(actors=query_param)
