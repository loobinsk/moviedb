from django.urls import path
from .views import form, test


urlpatterns = [
    path('add_compilation/', form),
    path('', test),
]
