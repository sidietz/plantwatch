from django.urls import path, include
from .views import PlantsList, PlantList, PlantList2, BlocksList, BlockView, impressum, random_plant, compliance, widmung, enemies, friends

urlpatterns = [
    path('', PlantsList.as_view(), name='index'),
    path('impressum', impressum, name="impressum"),
    path('compliance', compliance, name="compliance"),
    path('widmung', widmung, name="widmung"),
    path('enemies', enemies, name="enemies"),
    path('Feinde', enemies, name="Feinde"),
    path('friends', friends, name="friends"),
    path('Freunde', friends, name="Freunde"),
    path('block/<str:pk>/', BlockView.as_view(), name='block'),
    path('plant/', random_plant, name="random_plant"),
    path('blocks/', BlocksList.as_view(), name='blocks'),
    path('plants/', PlantsList.as_view(), name="plants"),
    path('plant/<plantid>/', PlantList.as_view(), name="plant"),
    path('plant2/<plantid>/', PlantList2.as_view(), name="plant2"),
]
