import datetime

from django.db import models


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.IntegerField()  # year

    def __str__(self):
        return self.first_name

    @property
    def age(self):
        return datetime.datetime.now().year - self.birthday


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def genre_str(self):
        return [i.name for i in self.genres.all()]
