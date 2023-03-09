from django.urls import path
from .views import *

urlpatterns = [
    path('create-game/', create_game, name='create_game'),
    path('attack-ship/', attack_ship, name='attack_ship'),
]
