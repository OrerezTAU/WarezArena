from django.urls import path
from . import views
from cracken.views import index

urlpatterns = [
    path('', index, name='index'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('warezgroups/', views.WarezGroupListView.as_view(),name="warez-groups"),
    path('warezgroup/<int:pk>', views.WarezGroupDetailView.as_view(), name='warez-group-detail'),
    path('stores/', views.StoreListView.as_view(),name="stores"),
    path('store/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
]

