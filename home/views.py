from django.shortcuts import render
from objects.models import Compilation, Genre, Picture, Actor
from objects.parser import Parser
import requests
from bs4 import BeautifulSoup
from django.db.models import Count
from embed_video.backends import detect_backend
from django.db.models import F


genres = Genre.objects.annotate(count=Count('collections_genre')).order_by('-count')[:15]

def homepage(request):
	template = 'base.html'

	new_collections = Compilation.objects.all().order_by('-created')[:5]
	popular_collections = Compilation.objects.all().order_by('-views')[:5]

	# for i in Picture.objects.all():
	# 	i.delete()
	# for i in Compilation.objects.all():
	# 	i.delete()

	context = {
		'new_collections': new_collections,
		'popular_collections': popular_collections,
		'genres': genres,
		}

	return render(request, template, context)

def search_page(request):
	template = 'catalog.html'

	query = request.POST['query']
	collections = Compilation.objects.filter(name__search=query)
	print(collections)

	title = f'Подборки по запросу "{query}"'

	context = {
		'title': title,
		'genres': genres,
		'query': query,
		'collections':collections
		}
	return render(request, template, context)

def collection_detail(request, slug):
	template = 'collection_detail.html'

	collection = Compilation.objects.get(slug=slug)
	collection.views += 1
	collection.save()
	best_films = Picture.objects.filter(collections=collection).order_by('-rating_kinopoisk')[:10]
	new_films = Picture.objects.filter(collections=collection).order_by('-released')[:10]
	popular_collections = Compilation.objects.all().order_by('-views').exclude(slug=slug)[:5]

	context = {
		'collection': collection,
		'best_films': best_films,
		'new_films': new_films,
		'genres': genres,
		'popular_collections': popular_collections,
		}
	return render(request, template, context)


def film_detail(request, slug):
	template = 'picture_detail.html'

	new_collections = Compilation.objects.all().order_by('-created')[:5]
	popular_collections = Compilation.objects.all().order_by('-views')[:5]
	picture = Picture.objects.get(slug=slug)

	context = {
		'new_collections': new_collections,
		'popular_collections': popular_collections,
		'picture': picture,
		'genres': genres,
		}
	return render(request, template, context)

def actors_list(request):
	template = 'catalog.html'

	all_actors = Actor.objects.all()[:500]

	title = 'Все актеры'

	context = {
			'all_actors': all_actors,
			'genres': genres,
			'title': title,
		}
	return render(request, template, context)

def collection_list(request, genre=None):
	template = 'catalog.html'

	genre_name = None
	if genre:
		genre = Genre.objects.get(slug=genre)
		genre_name = genre.name
		all_collections = Compilation.objects.filter(main_genre=genre).order_by('views')[:500]
		title = 'Все подборки по жанру '+genre_name
	else:
		all_collections = Compilation.objects.all().order_by('views')[:500]
		title = 'Все подборки'

	context = {
		'title': title,
		'genre': genre_name,
		'genres': genres,
		'all_collections': all_collections
		}
	return render(request, template, context)

def film_list(request):
	template = 'catalog.html'

	all_films = Compilation.objects.filter(type_collections=0).order_by('-views')[:100]

	title = 'Все подборки фильмов'

	context = {
		'title': title,
		'genres': genres,
		'all_films': all_films,
		}
	return render(request, template, context)

def series_list(request):
	template = 'catalog.html'

	all_series = Compilation.objects.filter(
		type_collections=1).order_by('-views')[:100]

	title = 'Все подборки сериалов'

	context = {
		'title': title,
		'genres': genres,
		'all_series': all_series,
		}
	return render(request, template, context)

def cartoons_list(request):
	template = 'catalog.html'

	all_cartoons = Compilation.objects.filter(
		type_collections=2).order_by('-views')[:100]

	title = 'Все подборки мультфильмов'

	context = {
		'title': title,
		'genres': genres,
		'all_cartoons': all_cartoons,
		}
	return render(request, template, context)

def anime_list(request):
	template = 'catalog.html'

	all_anime = Compilation.objects.filter(
		type_collections=3).order_by('-views')[:100]

	title = 'Все подборки аниме'

	context = {
		'title': title,
		'genres': genres,
		'all_anime': all_anime,
		}
	return render(request, template, context)