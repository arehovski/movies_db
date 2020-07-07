from django.shortcuts import render
from django import views
from django.views.generic import ListView
from .models import Actor, Director, Movie, Genre, Country, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from .forms import RegistrationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity


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
            'user': request.user
        }
        return render(request, self.template, context)


class GenreView(views.View):
    template = "genre.html"

    @staticmethod
    def get_movies(query_param):
        return Movie.objects.filter(genre__genre=query_param)

    def get(self, request, param):
        movies = self.get_movies(param)
        movies = pagination(movies, request)
        context = {
            'movies': movies,
            'user': request.user,
            'param': param
        }
        return render(request, self.template, context=context)


class YearView(GenreView):
    template = 'year.html'
    @staticmethod
    def get_movies(query_param):
        return Movie.objects.filter(year=query_param)


class CountryView(GenreView):
    template = 'country.html'
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
            'similar_movies': similar_movies,
            'user': request.user
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
            'related_movies': related_movies,
            'user': request.user
        }
        return render(request, self.template, context)


class ActorView(DirectorView):
    template = 'actor.html'
    model = Actor

    @staticmethod
    def get_related_movies(query_param):
        return Movie.objects.filter(actors=query_param)


class RegistrationView(views.View):
    template = 'registration.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_page')
        form = RegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.save()
            auth_user = authenticate(request, username=user_data['username'], password=user_data['password'])
            login(request, auth_user)
            return redirect('home_page')
        return render(request, self.template, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')


class LoginView(views.View):
    template = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_page')
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
        return render(request, self.template, {'form': form})


class SearchView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10
    template_name = 'search.html'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=f"{self.request.GET.get('query')}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        return context


def add_to_wish_list(request, pk):
    movie = Movie.objects.get(pk=pk)
    user = request.user
    if user.is_authenticated:
        user.wish_list.add(movie)
        messages.success(request, 'Фильм добавлен в папку "Избранное"')
        referer = request.headers.get("Referer")
        if referer:
            return redirect(referer)
        else:
            return redirect('/')
    else:
        return redirect('login')


def remove_from_wish_list(request, pk):
    movie = Movie.objects.get(pk=pk)
    user = request.user
    if user.is_authenticated:
        wish_list = user.wish_list.all()
        if movie in wish_list:
            user.wish_list.remove(movie)
            messages.warning(request, 'Фильм удален из папки "Избранное"')
        referer = request.headers.get("Referer")
        if referer:
            return redirect(referer)
        else:
            return redirect('/')
    else:
        return redirect('login')


class WishListView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 20
    template_name = 'wish_list.html'

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user.pk).order_by('-wishlist')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login')
