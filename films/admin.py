from django.contrib import admin
from films.models import Movie, Director, Genre

# Register your models here.

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Genre)
