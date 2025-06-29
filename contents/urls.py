from django.urls import path
from .views import *

app_name = 'contents'

urlpatterns = [
    path('', main, name='main'),
    path('create/', create, name='create'),
]