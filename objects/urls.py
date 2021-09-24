from django.urls import path
from .views import form


urlpatterns = [
    path('add_compilation/', form),
]
