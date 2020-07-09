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
    path('search', SearchView.as_view(), name='search'),
    path('add_movie/<int:pk>', add_to_wish_list, name='add_movie'),
    path('rm_movie/<int:pk>', remove_from_wish_list, name='rm_movie'),
    path('wish_list', WishListView.as_view(), name='wish_list'),
    path('api/movie_list', MovieList.as_view(), name='api_list')
]
