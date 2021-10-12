from django.urls import path
from .views import form, test, form_detail


urlpatterns = [
    path('add_compilation/', form, name='form'),
    path('add_compilation_detail/', form_detail, name='form_detail'),
    path('', test),
]
