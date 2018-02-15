from django.urls import path
from . import views


urlpatterns = [
    path('', views.blocks, name='index'),
    path('impressum', views.impressum, name="impressum"),
    path('blocks/', views.blocks, name='blocks'),
    path('block/<blockid>/', views.block, name='block'),
    path('plant/<plantid>/', views.plant, name="plant"),
    path('plant/', views.plant, name="plant"),
    path('plants/', views.plants, name="plants"),

]

