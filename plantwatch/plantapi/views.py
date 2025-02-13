from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from .serializers import PlantSerializer, BlockSerializer, PollutantSerializer, PollutionSerializer
from plantmaster.models import Blocks, Plants, Pollutions



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

class PollutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blocks to be viewed.
    """
    queryset = Pollutions.objects.all().order_by('-year').order_by('plantid').order_by('pollutant')
    serializer_class = PollutantSerializer

class PollutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blocks to be viewed.
    """
    queryset = Pollutions.objects.all().order_by('-year').order_by('plantid').order_by('pollutant')
    serializer_class = PollutantSerializer

def pollution_by_plantid(request, pk):
    queryset = Pollutions.objects.filter(plantid=pk).order_by('-year').order_by('plantid').order_by('pollutant')
    serializer = PollutionSerializer(queryset, pk)
    return serializer.data

class PollutionList(generics.ListAPIView):
    serializer_class = PollutionSerializer

    def get_queryset(self):
        plantid = self.kwargs['plantid']
        queryset = Pollutions.objects.filter(plantid=plantid).order_by('pollutant').order_by('-year')
        return queryset

class PollutionList2(generics.ListAPIView):
    serializer_class = PollutionSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        queryset = Pollutions.objects.filter(year=year).order_by('-amount')
        return queryset
    
    
