from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

class Genre(models.Model):
	'''Жанр фильма'''
	name = models.CharField(max_length=255)
	slug = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def save(self):
		self.slug = slugify(unidecode(self.name))
		super(Genre, self).save()

class Country(models.Model):
	''' Страна фильма '''
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Actor(models.Model):
	''' Актер '''
	url_photo = models.TextField()
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
	genres = models.ManyToManyField(Genre)
	duration = models.IntegerField('Длительность', blank=True, null=True)
	minimum_age = models.IntegerField('Минимальный возраст', blank=True, null=True)
	type_picture = models.PositiveSmallIntegerField(choices=TYPE_PICTURE, blank=True, null=True)
	premiere_in_Russia = models.CharField('Премьера в России', max_length=255, blank=True, null=True)
	rating_kinopoisk = models.FloatField('рейтинг от кинопоиска', blank=True, null=True)
	rating_imdb = models.FloatField('рейтинг от IMDB', blank=True, null=True)
	facts = models.TextField('список фактов', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.name_in_russian}, {self.released}, {self.id}'

class Compilation(models.Model):
	''' Подборка картин '''
	poster = models.ImageField('постер подборки', blank=True, null=True)
	pictures = models.ManyToManyField(Picture)
	name = models.CharField(max_length=255, blank=True, null=True)
	views = models.IntegerField('Кол-во просмотров подборки', default=0)
	created = models.DateTimeField('Дата создания', auto_now_add=True)

	def __str__(self):
		return self.name

# class Frame(models.Model):
# 	''' Кадр картины '''
# 	picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
# 	url = models.TextField('ссылка на кадр')

# 	def __str__(self):
# 		return self.picture.name_in_russian




