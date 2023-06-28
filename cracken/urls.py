from django.urls import path
from . import views
from cracken.views import index, game, warez_group, store, game_detail, warez_group_detail, store_detail

urlpatterns = [
    path('', index, name='index'),
    path("games/", game, name="games"),
    path("games/<int:pk>/", game_detail, name="game_detail"),
    path("warez_groups/", warez_group, name="warez_groups"),
    path("warez_groups/<int:pk>/", warez_group_detail, name="warez_group_detail"),
    path("stores/", store, name="stores"),
    path("stores/<int:pk>/", store_detail, name="store_detail"),
]

