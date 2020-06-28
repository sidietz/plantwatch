from django.contrib import admin
from django.urls import path, include

PLANTMASTER = 'plantmaster.urls'

urlpatterns = [
    path('', include(PLANTMASTER)),
    path('plantmaster/', include(PLANTMASTER)),
    path('plantwatch/', include(PLANTMASTER)),
    path('plantapi/', include('plantapi.urls')),
    path('admin/', admin.site.urls),
]
