from django.shortcuts import render, redirect
from .parser import Parser
from django.http import HttpResponse
from .models import Country
import requests
from django.contrib.auth.decorators import login_required


@login_required
def form(request):
	template = 'admin/form.html'

	message = None
	if request.method == 'POST':
		list_complitation = request.FILES['file'].readlines()
		min_count = int(request.POST['min_count'])
		max_count = int(request.POST['max_count'])
		for i in list_complitation:
			name_complit = i.decode('utf-8')
			parse = Parser(name_complit, min_number=min_count, max_number=max_count)
			parse.data_processing()
		message = f'Создано подборок: {len(list_complitation)}шт, можете проверить.'

	context = {'message': message,
				'count': range(0,80)}
	return render(request, template, context)

def test(request):
	parse = Parser('фильмы про постапокалипсис')
	parse.data_processing()
	return HttpResponse('все окей')
