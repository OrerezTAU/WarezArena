from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import GameSerializer, WarezGroupSerializer, StoreSerializer
from .models import Game, WarezGroup, Store


# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


# ------------------------------------------------------------------------------------
# API views

# POST and GET methods:

# We check for type of request method.
# If it is a get method we query the database to retrieve all the available instances of model,
# and then we serialize the data received from the database, then return the serialized data to the frontend
# for display. Else if it is a post method, we deserialize the data received from the frontend, then save it to the
# database.
@api_view(['GET', 'POST'])
def game(request):
    """This is the view for the Game model."""
    if request.method == 'GET':
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def warez_group(request):
    """This view is for the WarezGroup model."""
    if request.method == 'GET':
        group = WarezGroup.objects.all()
        serializer = WarezGroupSerializer(group, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WarezGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def store(request):
    """This view is for the Store model."""
    if request.method == 'GET':
        group = Store.objects.all()
        serializer = StoreSerializer(group, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE methods:


@api_view(['DELETE'])
def game_detail(request, pk):
    try:
        my_game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        my_game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def warez_group_detail(request, pk):
    try:
        group = WarezGroup.objects.get(pk=pk)
    except WarezGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def store_detail(request, pk):
    try:
        my_store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        my_store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
