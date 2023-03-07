from django.urls import path
from .views import *

urlpatterns = [
    path('create-game/', CreateGame.as_view(), name='create_game'),
]
