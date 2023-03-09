from rest_framework import serializers
from .models import Game, Ship


class DetailsSerializer(serializers.Serializer):
    details = serializers.CharField()
    
    class Meta:
        fields = '__all__'


class AttackRequestSerializer(serializers.Serializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())
    attacking_ship = serializers.PrimaryKeyRelatedField(queryset=Ship.objects.all())
    targeted_ship = serializers.PrimaryKeyRelatedField(queryset=Ship.objects.all())
    
    class Meta:
        fields = '__all__'


class ShipSerializer(serializers.ModelSerializer):
    captain = serializers.CharField(source='captain.name')
    
    class Meta:
        model = Ship
        fields = '__all__'


class GameSerializer(serializers.Serializer):
    name = serializers.CharField()
    ships = ShipSerializer(source='ship_set', many=True)
    
    class Meta:
        fields = '__all__'