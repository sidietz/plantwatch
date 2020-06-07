from django.urls import path, include
from .views import *

urlpatterns = [
    path('', plants, name='index'),
    path('impressum', impressum, name="impressum"),
    path('blocks/', blocks, name='blocks'),
    path('block/<blockid>/', block, name='block'),
    path('plant/<plantid>/', plant, name="plant"),
    path('plant2/<plantid>/', plant2, name="plant2"),
    path('plant/', random_plant, name="random_plant"),
    path('plants/', plants, name="plants"),
]
