from django.shortcuts import render
from rest_framework import generics, status, response
from .serializers import DetailsSerializer, AttackRequestSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import logging
from utils.exception_handler import BadRequestException, ServerErrorException
from .models import Game, Ship, Captain
from faker import Faker
from rest_framework.decorators import api_view


logger = logging.getLogger('stderr')


@extend_schema(
    responses={201: DetailsSerializer},
    parameters=[
        OpenApiParameter(
            name='ships',
            type=OpenApiTypes.STR,
            description='Number of ships to create in the game, with the number of soldiers onboard. Numbers from 1 to 100 are allowed.',
            examples=[
                OpenApiExample(
                    'Example 1',
                    summary='Create 4 ships',
                    description='The format of this query parameter value should always be a string with numbers separated by commas. '
                                'Every number represents one ship and the size of that number represents number of soldiers on that particular vessel. '
                                'Feel free to put in some other values.',
                    value='50,58,68,40'
                )
            ]
        )
    ]
)
@api_view(['GET'])
def create_game(request):
    ships = request.query_params.get('ships')
    ships = ships.split(',')
    try:
        soldiers_on_ship = [int(soldiers) for soldiers in ships if 1 <= int(soldiers) <= 100]
    except Exception as ex:
        logger.error(str(ex))
        raise BadRequestException(detail='Only numbers and commas are allowed')
    
    if len(soldiers_on_ship) != len(ships):
            raise BadRequestException(detail='Invalid value(s) for soldiers on ship.')
    
    if soldiers_on_ship is None:
        raise BadRequestException(detail='There was a problem while getting number of soldiers')
    else:
        try:
            game = Game.objects.create()
            fake = Faker()
            
            for num_of_soldiers in soldiers_on_ship:
                ship = Ship.objects.create(soldiers=num_of_soldiers, game=game)
                Captain.objects.create(name=fake.name(), rank='Captain', ship=ship)
        except Exception as ex:
            logger.error(str(ex))
            raise ServerErrorException(detail='Problem while creating game.')
    
    res = {'details': f'{len(soldiers_on_ship)} ships were created in {game.name}'}
    serialized = DetailsSerializer(res)
    
    return response.Response(serialized.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request= AttackRequestSerializer,
    responses={200: DetailsSerializer}
)
@api_view(['POST'])
def attack_ship(request):
    res = dict()
    
    data_serialized = AttackRequestSerializer(data=request.data)
    data_serialized.is_valid(raise_exception=True)
    data = data_serialized.validated_data
    
    attacking_ship = data['attacking_ship']
    targeted_ship = data['targeted_ship']
    game = data['game']
    
    if game.game_ended is True:
        res['details'] = game.winner()
        serialized = DetailsSerializer(res)
        return response.Response(serialized.data, status=status.HTTP_200_OK)
    
    if attacking_ship.game != game or targeted_ship.game != game:
        raise BadRequestException(detail='You must select ships that are in the same game you sent')
    
    if attacking_ship == targeted_ship:
        raise BadRequestException(detail='You must select different ships for battle')
    
    if attacking_ship.has_sunk():
        raise BadRequestException(detail='Attacking ship has sunk')
    
    if targeted_ship.has_sunk():
        raise BadRequestException(detail='The ship you were targeting is no longer a threat, as it has sunk')
    
    attacking_ship.attack(targeted_ship)
    
    if targeted_ship.has_sunk() is True:
        res['details'] = f'Attacking ship health: {attacking_ship.health}. Targeted ship with id {targeted_ship.id} has sunk'
    else:
        targeted_ship.attack(attacking_ship)
    
    if attacking_ship.has_sunk() is True:
        res['details'] = f'Attacking ship with id {attacking_ship.id} has sunk. Targeted ship health: {targeted_ship.health}'
    
    if attacking_ship.has_sunk() is False and targeted_ship.has_sunk() is False:
        res['details'] = f'Attacking ship health: {attacking_ship.health}. Targeted ship health: {targeted_ship.health}'
    
    if game.has_ended() is True:
        res['details'] = game.winner()
    
    serialized = DetailsSerializer(res)
    
    return response.Response(serialized.data, status=status.HTTP_200_OK)
