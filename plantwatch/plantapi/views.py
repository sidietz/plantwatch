from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import PlantSerializer, BlockSerializer
from plantmaster.models import Blocks, Plants



class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plants to be viewed.
    """
    queryset = Plants.objects.all().order_by('-totalpower')
    serializer_class = PlantSerializer


class BlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blocks to be viewed.
    """
    queryset = Blocks.objects.all().order_by('-netpower')
    serializer_class = BlockSerializer
