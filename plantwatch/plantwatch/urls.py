from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('plantmaster.urls')),
    path('plantmaster/', include('plantmaster.urls')),
    path('plantwatch/', include('plantmaster.urls')),
    path('plantapi/', include('plantapi.urls')),
    path('admin/', admin.site.urls),
]
