from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('genres/<param>', GenreView.as_view(), name='genre_view'),
    path('year/<param>', YearView.as_view(), name='year_view'),
    path('country/<param>', CountryView.as_view(), name='country_view'),
    path('movie/<int:pk>', MovieView.as_view(), name='movie_view'),
    path('director/<int:pk>', DirectorView.as_view(), name='director_view'),
    path('actor/<int:pk>', ActorView.as_view(), name='actor_view'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
]