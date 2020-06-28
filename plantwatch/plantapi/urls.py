from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import BlockViewSet, PlantViewSet

router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet)
router.register(r'blocks', BlockViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls')),
]

'''
path('block/<blockid>/', views.block, name='block'),
    path('plant/<plantid>/', views.plant, name="plant"),
    path('plant/', views.plant, name="plant"),
    path('plants/', views.plants_2, name="plants"),
'''
