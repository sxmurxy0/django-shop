from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views._login, name='login'),
    path('logout/', views._logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]