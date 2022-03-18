from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.home_create, name='create'),
    path('log_user', views.log_user, name='log_user'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('account/<int:user_id>', views.account, name='account'),
    path('add_food', views.add_food, name='add_food'),
]
