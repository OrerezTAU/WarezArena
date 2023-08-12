import django_tables2 as tables
from .models import Store, Game, WarezGroup


class StoreTable(tables.Table):
    class Meta:
        model = Store
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "url", "description")


class GameTable(tables.Table):
    class Meta:
        model = Game
        template_name = "django_tables2/bootstrap.html"
        linkify = ("cracking_group",)
        fields = ("name", "cracking_group", "crack_date", "available_on_stores", "score", "num_reviews", "nfo_link")

    available_on_stores = tables.ManyToManyColumn(linkify_item=True)


class WarezGroupTable(tables.Table):
    class Meta:
        model = WarezGroup
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "year_founded", "description")
