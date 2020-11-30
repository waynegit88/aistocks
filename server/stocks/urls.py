from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    path('add_user/', add_user, name='add_user'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('save_selected/', save_selected, name='save_selected'),
    path('get_csrf/', get_csrf, name='get_csrf'),
    path('get_stocklist/', get_stocklist, name='get_stocklist'),
    path('get_kline/', get_kline, name='get_kline'),
]
