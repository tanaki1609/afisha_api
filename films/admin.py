from django.contrib import admin
from .models import Film, Director, Genre, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class FilmAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    search_fields = ['name']
    list_filter = ['director', 'genres']
    list_display = ['name', 'director', 'is_active', 'created']
    list_editable = ['is_active']


admin.site.register(Film, FilmAdmin)
admin.site.register(Director)
admin.site.register(Genre)
