from rest_framework import serializers
from .models import Game, WarezGroup, Store


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class WarezGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarezGroup
        fields = ('id', 'name', 'description', 'year_founded')


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'url', 'description')

