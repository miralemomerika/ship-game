from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game
from .views import GameView


class GameViewTestCase(APITestCase):
    def setUp(self):
        self.game1 = Game.objects.create()
        self.game2 = Game.objects.create(game_ended=True)
        self.game3 = Game.objects.create()
    
    def test_ended_games(self):
        view = GameView.as_view()
        response = self.client.get(reverse('all_games'), {'game_ended': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.game2.name)
    
    def test_active_games(self):
        view = GameView.as_view()
        response = self.client.get(reverse('all_games'), {'game_ended': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)