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
	prs = Parser()
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

	context = {
		'genres': genres,
		'query': query,
		'collections':collections
		}
	return render(request, template, context)

def collection_detail(request, pk):
	prs = Parser()
	template = 'collection_detail.html'

	collection = Compilation.objects.get(pk=pk)
	collection.views += 1
	collection.save(update_fields=['views'])
	best_films = Picture.objects.filter(collections=collection).order_by('-rating_kinopoisk')[:15]
	new_films = Picture.objects.filter(collections=collection).order_by('-released')[:15]
	popular_collections = Compilation.objects.all().order_by('-views').exclude(pk=pk)[:5]

	context = {
		'collection': collection,
		'best_films': best_films,
		'new_films': new_films,
		'genres': genres,
		'popular_collections': popular_collections,
		}
	return render(request, template, context)


def film_detail(request, pk):
	template = 'picture_detail.html'

	new_collections = Compilation.objects.all().order_by('-created')[:5]
	popular_collections = Compilation.objects.all().order_by('-views')[:5]
	picture = Picture.objects.get(pk=pk)

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

	context = {
			'all_actors': all_actors,
			'genres': genres,
		}
	return render(request, template, context)

def collection_list(request, genre=None):
	template = 'catalog.html'

	genre_name = None
	if genre:
		genre = Genre.objects.get(slug=genre)
		genre_name = genre.name
		all_collections = Compilation.objects.filter(main_genre=genre).order_by('views')[:500]
	else:
		all_collections = Compilation.objects.all().order_by('views')[:500]

	context = {
		'genre': genre_name,
		'genres': genres,
		'all_collections': all_collections
		}
	return render(request, template, context)

def film_list(request):
	template = 'catalog.html'

	all_films = Picture.objects.all().order_by('-rating_kinopoisk')[:100]

	context = {
		'genres': genres,
		'all_films': all_films,
		}
	return render(request, template, context)

def series_list(request):
	template = 'catalog.html'

	all_series = Picture.objects.filter(
		type_picture=1).order_by('-rating_kinopoisk')[:100]

	context = {
		'genres': genres,
		'all_series': all_series,
		}
	return render(request, template, context)

def cartoons_list(request):
	template = 'catalog.html'

	all_cartoons = Picture.objects.filter(
		type_picture=2).order_by('-rating_kinopoisk')[:100]

	context = {
		'genres': genres,
		'all_cartoons': all_cartoons,
		}
	return render(request, template, context)

def anime_list(request):
	template = 'catalog.html'

	all_anime = Picture.objects.filter(
		type_picture=3).order_by('-rating_kinopoisk')[:100]

	context = {
		'genres': genres,
		'all_anime': all_anime,
		}
	return render(request, template, context)