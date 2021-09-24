from django.shortcuts import render, redirect
from .parser import Parser
from django.http import HttpResponse
from .models import Country
import requests

def form(request):
	template = 'admin/form.html'

	message = None
	if request.method == 'POST':
		try:
			list_complitation = request.FILES['file'].readlines()
			min_count = int(request.POST['min_count'])
			max_count = int(request.POST['max_count'])
			for i in list_complitation:
				name_complit = i.decode('utf-8')
				parse = Parser(name_complit, min_number=min_count, max_number=max_count)
				parse.data_processing()
			message = f'Создано подборок: {len(list_complitation)}шт, можете проверить.'
		except:
			message = 'Произошла ошибка! Пожалуйста, проверьте корректность введенных данных.'

	context = {'message': message}
	return render(request, template, context)
