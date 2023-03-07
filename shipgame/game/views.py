from django.shortcuts import render
from rest_framework import generics, status, response
from .serializers import GameSerializer
from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import logging


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
            for soldiers in ships:
                num_of_soldiers = int(soldiers)
        except Exception as ex:
            logger.error(str(ex))
        
        return response.Response('response msg', status=status.HTTP_200_OK)
