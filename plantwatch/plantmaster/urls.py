from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PlantsList.as_view(), name='index'),
    path('impressum', impressum, name="impressum"),
    path('block/<str:pk>/', BlockView.as_view(), name='block'),
    path('plant/', random_plant, name="random_plant"),
    path('blocks/', BlocksList.as_view(), name='blocks'),
    path('plants/', PlantsList.as_view(), name="plants"),
    path('plant/<plantid>/', PlantList.as_view(), name="plant"),
    path('plant2/<plantid>/', PlantList2.as_view(), name="plant2"),
]
