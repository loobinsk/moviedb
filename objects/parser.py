import random
import requests
import time
import json

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.templatetags.static import static

from fake_useragent import UserAgent

from .models import Genre, Country, Actor, Director
from .models import Picture, Compilation

from django.conf import settings

from django.utils.text import slugify
from unidecode import unidecode


class Parser():
	''' Принимает поисковой запрос,
		парсит яндекс,
		ищет фильм в апи кинопоиска,
		добавляет все данные в бд проекта
		'''
	def __init__(self, query, min_number=10, max_number=20):
		''' принимаем поисковой запрос '''

		#формируем ссылку на парсер яндекса
		number_films = random.randint(min_number, max_number)
		yandex_key = 'https://yandex.ru/search/xml?user=sniffer11&key=03.84419783:0d50a8be485b8062a4ef7a795f72fe69'
		request = f'url:https://www.kinopoisk.ru/film/* {query} -episodes'
		if 'сериал' in query:
			request = f'url:https://www.kinopoisk.ru/series/* {query} -episodes'
		number_films = f'&groupby=groups-on-page%3D{number_films}'
		self.URL = yandex_key+'&query='+request+'&l10n=ru'+number_films
		self.query = query

	def get_all_film_id(self):
		''' получить id всех фильмов из поисковой выдачи 
			согласно запросу '''

		#формируем url
		request = requests.get(self.URL)
		soup = BeautifulSoup(request.content, 'html.parser')
		links = soup.findAll('url')
		list_id = []

		for i in links:
			href = i.text.strip()
			href = href.split('/')
			list_id.append(href[4])

		return list_id

	def data_processing(self):
		''' Принимает список с id всех фильмов,
			обрабатывает и форматирует данные
			с апи кинопоиска в формат для платформы,
			добавляет все данные в бд проекта
			'''

		#id_list = self.get_all_film_id()
		id_list = ['54233', '4324','66546432','21321','43543','24341','7845','43234','21367',]
		main_url = 'https://api.kinopoisk.dev/movie?search='
		token = '&field=id&token=M4JG0H0-MF0M5C0-MTW0XKB-68EDB2S'

		new_complitation = None
		if not Compilation.objects.filter(name=self.query).exists():
			path = settings.MEDIA_ROOT
			slug = slugify(unidecode(self.query))
			path = path+'compilations/'+slug+'.jpg'
			out = open(path, 'wb')
			poster = requests.get(self.Parse_yandex_images(self.query))
			out.write(poster.content)
			out.close()

			new_complitation = Compilation(name=self.query,
										poster='compilations/'+slug+'.jpg',
									)
			new_complitation.save()

			for i in id_list:
				url = main_url+i+token

				JsonData = requests.get(url).text
				if 'id not found' not in JsonData:
					JsonData = json.loads(JsonData)

					#data announcement
					try:
						name_in_english = JsonData["alternativeName"] #название на английском
					except:
						name_in_english = None

					try:
						min_age = JsonData["ageRating"]
					except:
						min_age = None

					name_in_russian = JsonData["name"] #имя на русском
					facts = JsonData['facts']
					facts_list = None
					if facts != None:
						facts_list = []
						for i in facts:
							facts_list.append(list(i.values()))

					poster = list(JsonData["poster"].values())[0] #постер картины
					if poster == None:
						continue
					else:
						path = settings.MEDIA_ROOT
						name = ''
						if name_in_english != None:
							name = name_in_english
						else:
							name = name_in_russian
						slug = slugify(unidecode(name))
						path = path+'posters/'+slug+'.jpg'
						out = open(path, 'wb')
						poster = requests.get(poster)
						out.write(poster.content)
						out.close()
						poster = 'posters/'+slug+'.jpg'


					slogan = JsonData["slogan"] #слоган
					description = JsonData["description"] #описание
					released = JsonData["year"] #дата релиза
					try:
						trailer = list(JsonData["videos"]['trailers'][0].values())[1] #ссылка на трейлер
					except:
						trailer = None

					try:
						duration = JsonData['movieLength'] #длительность в минутах
					except:
						duration = None
						continue

					try:
						type_picture = JsonData["type"] #тип картины фильм/сериал

						if type_picture == "movie":
							type_picture = 0
						elif type_picture == "anime":
							type_picture = 3
						elif type_picture == "tv-series":
							type_picture = 1
						elif type_picture == "cartoon":
							type_picture = 2
						elif type_picture == 'animated-series':
							type_picture = 4
					except:
						type_picture = None
						continue

					try:
						premiere_russia = JsonData["premiere"]['russia'].split('-')[0] #Премьера в России
					except:
						premiere_russia = None
					rating_kinopoisk = JsonData["rating"]['kp']#рейт по версии кп
					rating_imdb = JsonData["rating"]['imdb'] #рейт по версии кп
					if rating_imdb == 0 and rating_kinopoisk == 0:
						continue


					new_picture = None
					if not Picture.objects.filter(name_in_english=name_in_english,
												name_in_russian=name_in_russian,
												poster=poster,
												slogan=slogan,
												description=description,
												released=released,
												duration=duration,
												#minimum_age=age,
												type_picture=type_picture,
												premiere_in_Russia=premiere_russia,
												rating_kinopoisk=rating_kinopoisk,
												rating_imdb=rating_imdb,
												).exists():

						new_picture = Picture(name_in_english=name_in_english,
					 	 						name_in_russian=name_in_russian,
					 	 						poster=poster,
					 	 						slogan=slogan,
					 	 						description=description,
					 	 						released=released,
					 	 						duration=duration,
					 	 						minimum_age=min_age,
					 	 						type_picture=type_picture,
					 	 						premiere_in_Russia=premiere_russia,
					 	 						rating_kinopoisk=rating_kinopoisk,
					 	 						rating_imdb=rating_imdb,
					 	 						trailer=trailer,
					 	 						facts=facts_list,
												)

						new_picture.save()

						genres = JsonData["genres"] #список жанров
						for i in genres:
							i = list(i.values())
							new_genre = None
							if not Genre.objects.filter(name=i[0]).exists():
								new_genre = Genre(name=i[0])
								new_genre.save()
							else:
								new_genre = Genre.objects.get(name=i[0])
								
							new_picture.genres.add(new_genre)

						countries = JsonData["countries"] #список стран
						for i in countries:
							i = list(i.values())
							new_contry = None
							if not Country.objects.filter(name=i[0]).exists():
								new_contry = Country(name=i[0])
								new_contry.save()
							else:
								new_contry = Country.objects.get(name=i[0])

							new_picture.country.add(new_contry)


						actors = JsonData["persons"][:5] #список актеров
						for i in actors:
							i = list(i.values())
							actor_name = i[1]
							if actor_name == None:
								actor_name = i[2]

							new_actor = None
							if not Actor.objects.filter(name=actor_name).exists():
								new_actor = Actor(name=actor_name,
												url_photo=i[3])
								new_actor.save()
							else:
								new_actor = Actor.objects.get(name=actor_name)
								
							new_picture.starring.add(new_actor)

							if i[4] == "director":
								new_director = None
								director_name = i[1]
								if not director_name:
									director_name = i[2]

								if not Director.objects.filter(name=director_name).exists():
									new_director = Director(name=director_name)
									new_director.save()
								else:
									new_director = Director.objects.get(name=i[1])
							new_picture.directors.add(new_director)

					if new_complitation:
						if new_picture:
							new_complitation.pictures.add(new_picture)
							print('СОЗДАЛ КАРТИНУ')
						else:
							get_picture = Picture.objects.get(name_in_english=name_in_english,
												name_in_russian=name_in_russian,
												poster=poster,
												slogan=slogan,
												description=description,
												released=released,
												duration=duration,
												#minimum_age=age,
												type_picture=type_picture,
												premiere_in_Russia=premiere_russia,
												rating_kinopoisk=rating_kinopoisk,
												rating_imdb=rating_imdb,
												)
							print('ПОЛУЧИЛ КАРТИНУ')
							new_complitation.pictures.add(get_picture)

		return True


	def Parse_yandex_images(self, query):
		''' принимает запрос, выдает первую попавшуюся картинку из Яндекса '''
		images = ['https://im0-tub-ru.yandex.net/i?id=358e49b4004d4b2343f61b8fbe42b27f-l&n=13', 
				'https://im0-tub-ru.yandex.net/i?id=a3913cbae9f538ed453847d500158c31-l&n=13', 
				'https://im0-tub-ru.yandex.net/i?id=532434ede783bedbbe19324fdaef707d-l&n=13',
				'https://im0-tub-ru.yandex.net/i?id=d219690e4ceb9ad7a68a1aee3b9d2e51-l&n=13',
				'https://im0-tub-ru.yandex.net/i?id=02fe70b316080b0f2c8db1e7e6f2b1f0-l&n=13',
				'https://im0-tub-ru.yandex.net/i?id=8cc35533a7f1d7e8ed47f316f9007151&n=13&exp=1',]
		seconds = random.randint(1, 5)
		print(seconds)
		url = 'https://yandex.ru/images/search?text='

		try:
			ua = UserAgent()
			headers = {'User-Agent': ua.random}
			request = requests.get(url+query+'&from=tabbar', headers=headers)

			soup = BeautifulSoup(request.content, 'html.parser')
			links = soup.findAll('div', class_='serp-item serp-item_type_search serp-item_group_search serp-item_pos_0 serp-item_scale_yes justifier__item i-bem')
			link = links[0].get('data-bem').split('{"url":"')[1].split('",')[0]
			print('спарсили картинку', link)
		except:
			print('не удалось спарсить')
			key = random.randint(0, 5)
			return images[key]


		time.sleep(seconds)
		return link

	def get_url_trailer(self):
		pass

		



		

