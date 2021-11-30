import re
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from collections import Counter
from django.contrib.postgres.search import SearchQuery, SearchVector
from taggit.managers import TaggableManager
from django.db.models import Count
from django.urls import reverse


class Genre(models.Model):
	'''Жанр фильма'''
	name = models.CharField(max_length=255)
	slug = models.SlugField(blank=True, max_length=255)
	image = models.ImageField(upload_to='genres/')

	def __str__(self):
		return self.name

	def save(self):
		self.slug = f'{self.id}-{slugify(unidecode(self.name))}'
		super(Genre, self).save()

	def get_genre_collections(self):
		return self.collections_genre.count()

	def get_absolute_url(self):
		return reverse('collection_list', args=[self.slug])

class Country(models.Model):
	''' Страна фильма '''
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Actor(models.Model):
	''' Актер '''
	url_photo = models.TextField(blank=True, null=True)
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Director(models.Model):
	''' Кинорежиссёр  '''
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

FILM = 0
SERIAL = 1
CARTOON = 2
ANIME = 3
ANIMATED_SERIES=4
TYPE_PICTURE = (
    (FILM, 'Film'),
    (SERIAL, 'Serial'),
    (CARTOON, 'Cartoon'),
    (ANIME, 'Anime'),
    (ANIMATED_SERIES, 'animated-series')
)

class Picture(models.Model):
	''' модель для картины (фильма, мультфильма, аниме)'''
	kinopoisk_id = models.IntegerField('айди кинопоиска')
	name_in_english = models.CharField('Название на английском', max_length=255, blank=True, null=True)
	name_in_russian = models.CharField('Название на русском', max_length=255, blank=True, null=True)
	poster = models.ImageField('постер', blank=True, null=True)
	slogan = models.TextField('слоган', blank=True, null=True)
	description = models.TextField('описание', blank=True, null=True)
	released = models.IntegerField('Год выпуска', blank=True, null=True)
	trailer = models.URLField('ссылка на трейлер', blank=True, null=True)
	directors = models.ManyToManyField(Director)
	country = models.ManyToManyField(Country)
	starring = models.ManyToManyField(Actor)
	genres = models.ManyToManyField(Genre, related_name='pictures')
	preview = models.ImageField(upload_to='previews/')
	similar_picture = models.ManyToManyField('self')
	duration = models.IntegerField('Длительность', blank=True, null=True, default=0)
	minimum_age = models.IntegerField('Минимальный возраст', blank=True, null=True)
	type_picture = models.PositiveSmallIntegerField('Тип картины',choices=TYPE_PICTURE, blank=True, null=True)
	premiere_in_Russia = models.CharField('Премьера в России', max_length=255, blank=True, null=True)
	rating_kinopoisk = models.FloatField('рейтинг от кинопоиска', blank=True, null=True)
	rating_imdb = models.FloatField('рейтинг от IMDB', blank=True, null=True)
	slug = models.SlugField(blank=True, max_length=255, null=True)
	facts = models.TextField('список фактов', blank=True, null=True)
	created = models.DateTimeField('Дата создания картины',auto_now_add=True)

	def get_tags(self):
		try:
			name = f'{self.released}, {self.genres.all()[0]}, {self.country.all()[0]}'
		except:
			name = f'{self.released}'
		return name

	def __str__(self):
		return f'{self.name_in_russian}, {self.released}, {self.id}'

	def get_name(self):
		try:
			name = f'{self.name_in_russian}, {self.released}, {self.genres.all()[0]}, {self.country.all()[0]}'
		except:
			name = f'{self.name_in_russian}, {self.released}'
		return name
		
	def get_absolute_url(self):
		return reverse('film_detail', args=[self.slug])

	def get_count_similar_pictures(self):
		return self.similar_picture.count()

	def get_best_similar_pictures(self):
		return self.similar_picture.order_by('-rating_kinopoisk')

	def get_new_similar_pictures(self):
		return self.similar_picture.order_by('-released')

	def save(self):
		self.slug = f'{self.id}-{slugify(unidecode(self.name_in_russian))}'[:50]
		super(Picture, self).save()

class PictureFrames(models.Model):
	picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
	frame = models.ImageField('Кадр', blank=True, null=True)

	def __str__(self):
		return f'кадр картины {self.picture.name_in_russian}'



FILM = 0
SERIAL = 1
CARTOON = 2
ANIME = 3
ANIMATED_SERIES=4
TYPE_COLLECTION = (
    (FILM, 'Film'),
    (SERIAL, 'Serial'),
    (CARTOON, 'Cartoon'),
    (ANIME, 'Anime'),
    (ANIMATED_SERIES, 'animated-series')
)

class Compilation(models.Model):
	''' Подборка картин '''
	description = models.TextField('Описание', blank=True, null=True)
	poster = models.ImageField('Постер подборки', blank=True, null=True)
	pictures = models.ManyToManyField(Picture, related_name='collections')
	name = models.CharField('Название',max_length=255, blank=True, null=True)
	type_collections = models.PositiveSmallIntegerField('Тип подборки',choices=TYPE_COLLECTION, blank=True, null=True)
	main_genre = models.ManyToManyField(Genre, related_name='collections_genre')
	main_genre_text = models.TextField()
	tags = TaggableManager()
	slug = models.SlugField(blank=True, max_length=255)
	views = models.IntegerField('Кол-во просмотров подборки', default=0)
	created = models.DateTimeField('Дата создания', auto_now_add=True)

	def __str__(self):
		return self.name

	def get_name(self):
		return self.name[0].upper() + self.name[1:]

	def get_absolute_url(self):
		return reverse('collection_detail', args=[self.slug])

	def get_collection_type_name(self):
		name = None
		if self.type_collections == 0:
			name = 'фильмов'
		elif self.type_collections == 1:
			name='сериалов'
		elif self.type_collections == 2:
			name='мультфильмов'
		elif self.type_collections == 3:
			name='аниме'
		elif self.type_collections == 4:
			name='аниме сериалов'

		return name

	def get_pictures_count(self):
		return self.pictures.count()

	def add_description(self):
		'''сформировать описание подборки'''
		min_rating_picture = self.pictures.filter(rating_kinopoisk__gt=2).order_by('rating_kinopoisk').first()
		min_rating_picture = min_rating_picture.rating_kinopoisk

		max_rating_picture = self.pictures.filter(rating_kinopoisk__gt=2).order_by('rating_kinopoisk').last()
		max_rating_picture = max_rating_picture.rating_kinopoisk

		new_film = self.pictures.all().order_by('released').first()
		old_film = self.pictures.all().order_by('released').last()

		min_duration_film = self.pictures.filter(duration__gt=40).order_by('duration').last()
		max_duration_film = self.pictures.filter(duration__gt=40).order_by('duration').first()

		try:
			text = f'Мы собрали для Вас подборку лучших фильмов по теме “{self.name}” \
с рейтингом от {min_rating_picture} и до {max_rating_picture}. \
Самый новый фильм - {old_film.released} года, \
самый старый фильм - {new_film.released} года. \
Продолжительность фильмов от {max_duration_film.duration} до {min_duration_film.duration} минут. \
Выбирайте фильм и приятного просмотра!'
		except:
			text = f'Выбирайте картину и приятного просмотра!'
		self.description = text
		super(Compilation, self).save()

	def add_main_genre(self):
		''' сформировать основной жанр подборки '''
		list_genres = []
		for i in self.pictures.all():
			for genre in i.genres.all():
				list_genres.append(genre.name)

		ctr = Counter(list_genres)
		genre1 = Genre.objects.get(name=list(ctr)[0])
		genre2 = Genre.objects.get(name=list(ctr)[1])
		self.main_genre.add(genre1)
		self.main_genre.add(genre2)
		super(Compilation, self).save()
		genres_list = []
		for i in self.main_genre.all():
			genres_list.append(i.name)

		genres_text = ' '.join(genres_list)
		self.main_genre_text = genres_text
		super(Compilation, self).save()

		return genres_text

	def add_tags(self):
		tags = self.name.split(' ')
		for tag in tags:
			self.tags.add(tag)

		super(Compilation, self).save()

	def get_similar_collections(self):
		collections_tags_ids = self.tags.values_list('id', flat=True)
		similar_collections = Compilation.objects.filter(tags__in=collections_tags_ids).exclude(id=self.id)
		similar_collections = similar_collections.annotate(same_tags=Count('tags')).order_by('-same_tags',)[:5]
		
		return similar_collections

	def save(self):
		self.slug = slugify(unidecode(self.name))[:50]
		super(Compilation, self).save()

class СollectionСategory(models.Model):
	name = models.CharField(max_length=255)
	image = models.ImageField('Картинка категории', blank=True, null=True)
	keywords = models.TextField()
	slug = models.SlugField(blank=True, null=True, max_length=255)
	collections = models.ManyToManyField(Compilation, blank=True, null=True)

	def get_keywords_list(self):
		list_ = self.keywords.split(', ')
		return list_

	def get_absolute_url(self):
		return reverse('themes_detail', args=[self.slug])

	def save(self):
		super(СollectionСategory, self).save()
		self.slug = slugify(unidecode(f'{self.name}-{self.pk}'))[:50]
		super(СollectionСategory, self).save()

	def __str__(self):
		return self.name




