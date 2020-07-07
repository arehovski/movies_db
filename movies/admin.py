from django.contrib import admin
from .models import Actor, Director, Movie, Genre, User

# Register your models here.
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(User)

