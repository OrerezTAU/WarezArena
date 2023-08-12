from django.shortcuts import render
from django.views import generic
from django_filters import FilterSet
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from cracken.models import Game, WarezGroup, Store
from .tables import StoreTable, GameTable, WarezGroupTable


# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate the html table from the database
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


class StoreDetailView(generic.DetailView):
    model = Store


class StoreListView(SingleTableView):
    model = Store
    table_class = StoreTable


class GameDetailView(generic.DetailView):
    model = Game


class GameFilter(FilterSet):
    class Meta:
        model = Game
        fields = {
            'name': ['icontains'],
            'crack_date': ['year__exact', 'month__exact', 'day__exact'],
            'score': ['gt'],
            'num_reviews': ['gt'],
        }


class FilteredGameListView(SingleTableMixin, FilterView):
    model = Game
    table_class = GameTable
    filterset_class = GameFilter
    template_name = "cracken/game_list.html"


class WarezGroupDetailView(generic.DetailView):
    model = WarezGroup


class WarezGroupListView(SingleTableView):
    model = WarezGroup
    table_class = WarezGroupTable


