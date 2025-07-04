from django.urls import path
from .views import *

app_name = 'contents'

urlpatterns = [
    path('', main, name='main'),
    path('create/', create, name='create_default'),
    path('create/<int:book_id>/', create, name='create'),
    path('books/search/', book_search, name='book_search'),
    path('books/select/', select_book, name='select_book'),
]