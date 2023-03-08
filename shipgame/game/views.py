from django.shortcuts import render
from rest_framework import generics, status, response
from .serializers import GameSerializer
from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import logging
from utils.exception_handler import BadRequestException, ServerErrorException
from .models import Game, Ship, Captain
from faker import Faker


logger = logging.getLogger('stderr')


class CreateGame(generics.GenericAPIView):
    serializer_class = GameSerializer
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='ships',
                type=OpenApiTypes.STR,
                description='Number of ships to create in the game, with the number of soldiers onboard',
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
    def get(self, request, *args, **kwargs):
        ships = request.query_params.get('ships')
        ships = ships.split(',')
        try:
            soldiers_on_ship = [int(soldiers) for soldiers in ships]
        except Exception as ex:
            logger.error(str(ex))
            raise BadRequestException(detail='Only numbers and commas are allowed')
        
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
            
        
        return response.Response(f'{len(soldiers_on_ship)} ships were created in {game.name}', status=status.HTTP_200_OK)
