import random
import requests, re
import time
import json

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.templatetags.static import static

from .models import Genre, Country, Actor, Director
from .models import Picture, Compilation

from django.conf import settings

from django.utils.text import slugify
from unidecode import unidecode
from fake_useragent import UserAgent



class Parser():
	''' Принимает поисковой запрос,
		парсит яндекс,
		ищет фильм в апи кинопоиска,
		добавляет все данные в бд проекта
		'''
	def __init__(self, query='что', min_number=10, max_number=20, specific_number=None):
		''' принимаем поисковой запрос '''

		#формируем ссылку на парсер яндекса
		number_films = random.randint(min_number, max_number)
		if specific_number:
			number_films = specific_number
		self.yandex_key = 'https://yandex.ru/search/xml?user=sniffer11&key=03.84419783:0d50a8be485b8062a4ef7a795f72fe69'
		self.request = f'url:https://www.kinopoisk.ru/film/* {query} -episodes'

		if 'ериал' in query and 'ильм' not in query:
			self.request = f'url:https://www.kinopoisk.ru/series/* {query} -episodes -film'
		elif 'ильм' in query and 'ериал' in query:
			self.request = f'url:https://www.kinopoisk.ru/* {query} -episodes -media -lists -like'
		elif 'ильм' in query and 'ериал' not in query:
			self.request = f'url:https://www.kinopoisk.ru/film/* {query} -episodes -series'

		self.number_films = f'&groupby=groups-on-page%3D{number_films}'
		self.URL = self.yandex_key+'&query='+self.request+'&l10n=ru'+self.number_films
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
		if not Compilation.objects.filter(name=self.query).exists():

			id_list = self.get_all_film_id()
			print(id_list)

			path = settings.MEDIA_ROOT
			slug = slugify(unidecode(self.query))[:60]
			path = path+'compilations/'+slug+'.jpg'
			out = open(path, 'wb')
			poster = requests.get(self.Parse_yandex_images(self.query))
			out.write(poster.content)
			out.close()

			new_complitation = Compilation(name=self.query,
										poster='compilations/'+slug+'.jpg',
									)
			new_complitation.save()
			new_complitation.add_tags()
			pictures = []
			for i in id_list:
				if self.create_picture(i) != False:
					picture = self.create_picture(i)
					pictures.append(picture)
					similar_pictures = self.add_all_similar_pictures(i)
					for i in similar_pictures:
						picture.similar_picture.add(i)

			self.add_pictures_in_collection(pictures, new_complitation)
			if new_complitation.pictures.count() < 1:
				new_complitation.delete()
			else:
				new_complitation.add_description()
				new_complitation.add_main_genre()

		return True

	def add_pictures_in_collection(self, pictures, collection):
		for i in pictures:
			collection.pictures.add(i)
		

	def create_picture(self, id_picture):
		main_url = 'https://api.kinopoisk.dev/movie?search='
		token = '&field=id&token=M4JG0H0-MF0M5C0-MTW0XKB-68EDB2S'
		url = main_url+id_picture+token

		JsonData = requests.get(url).text
		if 'id not found' not in JsonData:
			print('пошла обработка фильма', id_picture)
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
			if not name_in_russian:
				print('нет названия на русском')
				return False
			facts = JsonData['facts']
			facts_list = None
			if facts != None:
				facts_list = []
				for i in facts:
					facts_list.append(list(i.values()))

			poster = list(JsonData["poster"].values())[0] #постер картины
			if poster == None:
				print('нет постера, идем дальше')
				return False
			else:
				path = settings.MEDIA_ROOT
				name = ''
				if name_in_english:
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
			# try:
			# 	trailer = list(JsonData["videos"]['trailers'][0].values())[1] #ссылка на трейлер
			# except:
			# 	trailer = None

			try:
				duration = JsonData['movieLength'] #длительность в минутах
			except:
				duration = None
				if 'ериал' not in self.query:
					print('нет длительности, идем дальше')
					return False

			try:
				type_picture = JsonData["type"] #тип картины фильм/сериал

				if type_picture == "movie":
					type_picture = 0
				elif type_picture == "anime":
					type_picture = 3
				elif type_picture == "tv-series":
					type_picture = 1
				elif type_picture == "cartoon" or type_picture == "carton":
					type_picture = 2
				elif type_picture == 'animated-series':
					type_picture = 4
				elif type_picture == 'mini-series':
					type_picture=1
				else:
					type_picture = 0
			except:
				type_picture = None
				print('нет типа картины, идем дальше')
				return False

			try:
				premiere_russia = JsonData["premiere"]['russia'].split('-')[0] #Премьера в России
			except:
				premiere_russia = None
			rating_kinopoisk = JsonData["rating"]['kp']#рейт по версии кп
			rating_imdb = JsonData["rating"]['imdb'] #рейт по версии кп
			if rating_imdb == 0 and rating_kinopoisk == 0:
				print('нет рейтинга, идем дальше')
				return False


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
			 	 						facts=facts_list,
			 	 						kinopoisk_id=id_picture,
									)

				new_picture.save()
				self.get_trailer(new_picture)
				try:
					backdrop = JsonData["backdrop"]['url']
					reequest = requests.get(backdrop)
				except:
					reequest = requests.get(self.Parse_yandex_images(f'{new_picture.name_in_russian} {new_picture.released}'))
				path = settings.MEDIA_ROOT
				slug = slugify(unidecode(new_picture.name_in_russian))[:60]
				path = path+'banners/'+slug+'.jpg'
				out = open(path, 'wb')
				poster = reequest
				out.write(poster.content)
				out.close()
				new_picture.banner = 'banners/'+slug+'.jpg'
				new_picture.save(update_fields=['banner'])
				print('картина создана')

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
							new_director = Director.objects.get(name=director_name)
					new_picture.directors.add(new_director)
			else:
				new_picture = Picture.objects.get(name_in_english=name_in_english,
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
				print('картина получена')
		else:
			print('фильма нет в апи')
			return False

		return new_picture



	def Parse_yandex_images(self, query):
		''' принимает запрос, выдает первую попавшуюся картинку из Яндекса '''
		images = ['https://im0-tub-ru.yandex.net/i?id=358e49b4004d4b2343f61b8fbe42b27f-l&n=13', 
				'https://im0-tub-ru.yandex.net/i?id=a3913cbae9f538ed453847d500158c31-l&n=13', 
				'https://im0-tub-ru.yandex.net/i?id=532434ede783bedbbe19324fdaef707d-l&n=13',
				'https://im0-tub-ru.yandex.net/i?id=d219690e4ceb9ad7a68a1aee3b9d2e51-l&n=13',
				'https://im0-tub-ru.yandex.net/i?id=02fe70b316080b0f2c8db1e7e6f2b1f0-l&n=13',
				'https://im0-tub-ru.yandex.net/i?id=8cc35533a7f1d7e8ed47f316f9007151&n=13&exp=1',]

		seconds = random.randint(1, 5)
		url = 'https://yandex.ru/images/search?text='
		headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'Connection': 'keep-alive',
		'Host': 'market.yandex.ru',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
		}
		request = requests.get(url+query+'&isize=eq&iw=1920&ih=1080&from=tabbar', headers=headers)

		try:
			soup = BeautifulSoup(request.content, 'html.parser')
			links = soup.findAll('div', class_='serp-item serp-item_type_search serp-item_group_search serp-item_pos_0 serp-item_scale_yes justifier__item i-bem')
			link = links[0].get('data-bem').split('{"url":"')[1].split('",')[0]
			print('спарсили картинку', link)
		except:
			print('не удалось спарсить')
			print(request.text)
			key = random.randint(0, 5)
			return images[key]


		time.sleep(5)
		return link

	def add_all_similar_pictures(self, id_picture):
		''' принимает фильм, отправляет запрос в кинопоиск,
		получает все похожие картины на данный фильм.'''
		ua = UserAgent()
		time.sleep(5)
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
			'Connection': 'keep-alive',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'none',
			'Sec-Fetch-User': '?1',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': ua.chrome,
		}

		request = requests.get(f'https://www.kinopoisk.ru/film/{id_picture}/like/', headers=headers)
		soup = BeautifulSoup(request.content, 'html.parser')
		
		href = soup.findAll('a', class_='all')
		list_similar_pictures = []
		for i in href:
			scan_href = i.get('href')
			if len(scan_href) > 1:
				_id = scan_href.split('/')[2]
				print('ПОЛУЧИЛ ПОДОБНУЮ КАРТИНУ', _id)

				print('СОЗДАНИЕ ПОДОБНОЙ КАРТИНЫ')
				similar_picture = self.create_picture(_id)
				print('подобная картина', similar_picture)
				if similar_picture != False:
					print('добавление подобной картины')
					list_similar_pictures.append(similar_picture)

		print('СПИСОК ПОХОЖИХ КАРТИН ФИЛЬМА',id_picture, list_similar_pictures)
		return list_similar_pictures

	def get_trailer(self, picture):
		print('картина',picture.name_in_russian)
		json_content = None

		url = f'https://www.youtube.com/results?search_query={picture.name_in_russian}+{picture.released}+трейлер&sp=EgQQARgB'
		print(url)
		headers = {
					"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
					'x-youtube-client-name': '1',
					'x-youtube-client-version': '2.20200605.00.00',
				}
		token_page = requests.get(url, headers=headers).text
		json_text = re.findall(r'(\{"responseContext".+\{\}\}\}|\{"responseContext".+"\]\})', token_page)[0]
		text = json_text.split('videoId')[1]
		text = text[2:]
		video_id = text.split('"')[1]
		print(video_id)


		print('итоговый айди', video_id)
		picture.trailer = video_id
		picture.save(update_fields=['trailer'])

		return True


		

