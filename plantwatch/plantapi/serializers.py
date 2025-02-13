from rest_framework import serializers
from plantmaster.models import Blocks, Plants, Pollutions

class BlockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blocks
        fields = ['blockid', 'blockname', 'netpower', 'energysource', 'plantid']

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Plants
        fields = ['plantid', 'plantname', 'blockcount', 'totalpower', 'energysource', 'state', 'chp', 'initialop', 'latestexpanded', 'company', 'blocks']

class PollutantSerializer(serializers.HyperlinkedModelSerializer):
    #pollutants = PollutantSerializer(many=True)

    class Meta:
        model = Pollutions
        fields = ['pollutionsid', 'year', 'plantid', 'pollutant', 'amount']

class PollutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pollutions
        fields = ['pollutionsid', 'plantid', 'year', 'pollutant', 'amount', 'amount2', 'unit2']

