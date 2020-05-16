from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
]

'''
path('block/<blockid>/', views.block, name='block'),
    path('plant/<plantid>/', views.plant, name="plant"),
    path('plant/', views.plant, name="plant"),
    path('plants/', views.plants_2, name="plants"),
'''
