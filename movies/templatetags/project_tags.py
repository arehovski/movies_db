from django import template
from django.db.models import Count
from movies.models import Director, Actor, Genre, Country, Movie
from movies.forms import SearchForm


register = template.Library()


@register.inclusion_tag('templatetags/navigation_bar.html')
def navigation_bar():
    genres = Genre.objects.all().annotate(total=Count("movie")).order_by('-total')
    countries = Country.objects.all().annotate(total=Count('movie')).order_by('-total')[:8]
    years = Movie.objects.all().values('year').annotate(total=Count('year')).order_by('-total')[:10]
    return {
        "genres": genres,
        "years": years,
        "countries": countries
    }


@register.inclusion_tag('templatetags/search_form.html')
def search_form():
    return {'form': SearchForm()}


@register.filter
def format_rating(value):
    return round(value, 1)
