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
    path('food/<int:food_id>', views.food, name='food'),
    path("add/comment", views.add_comment, name='comment'),
    path('delete/comment/<int:comment_id>', views.delete_comment),
]
