from django.shortcuts import render
from django.views import generic

from cracken import utils
from cracken.models import Game, WarezGroup, Store


# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate the html table from the database
    utils.create_html_table()
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


class StoreDetailView(generic.DetailView):
    model = Store


class StoreListView(generic.ListView):
    model = Store
    paginate_by = 10


class GameDetailView(generic.DetailView):
    model = Game


class GameListView(generic.ListView):
    model = Game
    paginate_by = 10


class WarezGroupDetailView(generic.DetailView):
    model = WarezGroup


class WarezGroupListView(generic.ListView):
    model = WarezGroup
    paginate_by = 10
