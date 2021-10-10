from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),

    #list urls
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/<genre>/', views.collection_list, name='collection_list'),
    path('search/', views.search_page, name='search'),
    path('films/', views.film_list, name='films_list'),
    path('series/', views.series_list, name='series_list'),
    path('cartoons/', views.cartoons_list, name='cartoons_list'),
    path('anime/', views.anime_list, name='anime_list'),
    path('actors/', views.actors_list, name='actors'),
    path('films/<pk>/', views.film_detail, name='film_detail'),
    path('collection/<pk>/', views.collection_detail, name='collection_detail'),
]
