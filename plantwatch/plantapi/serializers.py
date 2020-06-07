from rest_framework import serializers
from plantmaster.models import *

class BlockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blocks
        fields = ['blockid', 'blockname', 'netpower', 'energysource', 'plantid']

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Plants
        fields = ['plantid', 'plantname', 'blockcount', 'totalpower', 'energysource', 'state', 'chp', 'initialop', 'latestexpanded', 'company', 'blocks']
