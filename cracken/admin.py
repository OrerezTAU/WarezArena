from django.contrib import admin

from .models import Game, WarezGroup, Store


class GameInline(admin.TabularInline):
    model = Game
    extra = 0


# Register the Admin classes for Game using the decorator
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'num_reviews', 'nfo_link', 'crack_date')
    list_filter = ('crack_date', 'num_reviews')
    fields = ['name', ('score', 'num_reviews'), 'nfo_link', 'crack_date', 'warez_group']


# Register the Admin classes for Store using the decorator
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'description')
    fields = ['name', 'url', 'description']


# Register the Admin classes for WarezGroup using the decorator
@admin.register(WarezGroup)
class WarezGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year_founded')
    fields = ('name', 'description', 'year_founded')
    inlines = [GameInline]
