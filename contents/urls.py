from django.urls import path
from .views import *

app_name = 'contents'

urlpatterns = [
    path('', intro, name='intro'),
    path('main/', main, name='main'),
    path('create/', create, name='create_default'),
    path('create/<int:book_id>/', create, name='create'),
    path('books/search/', book_search, name='book_search'),
    path('books/select/', select_book, name='select_book'),
    path('detail/<int:id>/', detail, name='detail'),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>/', delete, name='delete'),
    path('like/<int:review_id>/', like, name='like'),
    path('dislike/<int:review_id>/', dislike, name='dislike'),
    path('scrap/<int:review_id>/', scrap, name='scrap'),
    path('create-comment/<int:review_id>/', create_comment, name='create-comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),
    path('reviews/search/', search_reviews, name='search_reviews'),
    path('popular/', popular_reviews, name='popular_reviews'),
    path('filter/', filter_by_tags, name='filter_reviews'),
    path('cancel-scrap/<int:review_id>/', cancel_scrap, name='cancel_scrap'),

]