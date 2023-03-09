from django_filters import FilterSet, BooleanFilter
from .models import Game


class GameFilter(FilterSet):
    game_ended = BooleanFilter(field_name='game_ended', required=True)
    
    class Meta:
        model = Game
        fields = ['game_ended']