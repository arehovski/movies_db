from django.shortcuts import render
from django import views
from .models import Actor, Director, Movie, Genre, Country
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class HomePage(views.View):
    movies = Movie.objects.all()
    template = "base.html"

    def get(self, request):
        genres = Genre.objects.all().annotate(total=Count("movie")).order_by('-total')
        countries = Country.objects.all().annotate(total=Count('movie')).order_by('-total')[:8]
        years = Movie.objects.all().values('year').annotate(total=Count('year')).order_by('-total')[:10]
        paginator = Paginator(self.movies, 10)
        page = request.GET.get('page')
        try:
            self.movies = paginator.page(page)
        except PageNotAnInteger:
            self.movies = paginator.page(1)
        except EmptyPage:
            self.movies = paginator.page(paginator.num_pages)
        context = {
            'movies': self.movies,
            'genres': genres,
            'years': years,
            'countries': countries
        }
        return render(request, self.template, context)
