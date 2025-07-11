from django.urls import path
from .views import signup_view, CustomLoginView, mypage, my_scraps, my_reviews, emotion_stats
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('mypage/', mypage, name='mypage'),
    path('my-scraps/', my_scraps, name='my_scraps'),
    path('my-reviews/', my_reviews, name='my_reviews'),
    path('emotion-stats/', emotion_stats, name='emotion_stats'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('find-id/', views.find_id, name='find_id'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/image/delete/', views.delete_profile_image, name='delete_profile_image'),
]

