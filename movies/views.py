from django.shortcuts import render
from django import views
from .models import Actor, Director, Movie


# Create your views here.
class HomePage(views.View):
    def get(self, request):
        actors = Actor.objects.all()
        directors = Director.objects.all()
        movies = Movie.objects.all()
        context = {
            'actors': actors,
            'directors': directors,
            'movies': movies
        }
        return render(request, 'base.html', context)