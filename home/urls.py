from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),

    #list urls
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/themes/', views.themes_list, name='themes_list'),
    path('collections/themes/<themes_slug>/', views.themes_detail, name='themes_detail'),
    path('collections/films/', views.film_list, name='films_list'),
    path('collections/series/', views.series_list, name='series_list'),
    path('collections/cartoons/', views.cartoons_list, name='cartoons_list'),
    path('collections/anime/', views.anime_list, name='anime_list'),
    path('collections/<genre>/', views.collection_list, name='collection_list'),

    path('films/', views.films, name='films'),
    path('series/', views.series, name='series'),
    path('cartoons/', views.cartoons, name='cartoons'),
    path('anime/', views.anime, name='anime'),

    path('actors/', views.actors_list, name='actors'),
    path('film/<slug>/', views.film_detail, name='film_detail'),
    path('collection/<slug>/', views.collection_detail, name='collection_detail'),

    path('search/', views.search_page, name='search'),

]
