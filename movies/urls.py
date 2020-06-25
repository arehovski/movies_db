from django.urls import path
from .views import HomePage, GenreView, YearView, CountryView, MovieView


urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('genres/<genre>', GenreView.as_view(), name='genre_view'),
    path('year/<year>', YearView.as_view(), name='year_view'),
    path('country/<country>', CountryView.as_view(), name='country_view'),
    path('movie/<int:pk>', MovieView.as_view(), name='movie_view'),

]