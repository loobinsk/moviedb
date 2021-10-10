from django.contrib import admin
from . import models

class GenreAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug',]
	search_fields = ['name', 'slug',]

admin.site.register(models.Genre, GenreAdmin)

class CountryAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']

admin.site.register(models.Country, CountryAdmin)

class ActorAdmin(admin.ModelAdmin):
	list_display = ['name', 'url_photo']
	search_fields = ['name']

admin.site.register(models.Actor, ActorAdmin)

class DirectorAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']

admin.site.register(models.Director, DirectorAdmin)

class PictureAdmin(admin.ModelAdmin):
	list_display = ['name_in_russian', 'minimum_age', 'slogan', 'released', 'get_count_similar_pictures', 'type_picture', 'rating_kinopoisk', 'created']
	list_filter = ['released', 'type_picture']
	search_fields = ['name_in_english', 'name_in_russian', 'slogan']

admin.site.register(models.Picture, PictureAdmin)

class CompilationAdmin(admin.ModelAdmin):
	list_display = ['name', 'views', 'created', 'get_pictures_count']
	search_fields = ['name']

admin.site.register(models.Compilation, CompilationAdmin)