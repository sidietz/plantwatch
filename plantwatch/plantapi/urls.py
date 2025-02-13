from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from .views import BlockViewSet, PlantViewSet, PollutionViewSet, PollutionList, PollutionList2

router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'pollutions', PollutionViewSet)
#router.register(r'', PollutionList.as_view(), basename='pollutant')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls')),
    re_path('^pollution/by_plantid/(?P<plantid>.+)/', PollutionList.as_view()),
    re_path('^pollution/by_year/(?P<year>.+)/', PollutionList2.as_view())
]

'''
path('block/<blockid>/', views.block, name='block'),
    path('plant/<plantid>/', views.plant, name="plant"),
    path('plant/', views.plant, name="plant"),
    path('plants/', views.plants_2, name="plants"),
'''
