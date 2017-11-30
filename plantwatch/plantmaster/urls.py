from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blocks/', views.blocks, name='blocks'),
    path('blocks/<int:lower>-<int:upper>-<int:code>/', views.blocks, name='blocks'),
    path('block/<blockid>/', views.block, name='block'),
]

'''
re_path(r'blocks/(lignite|coal|gas)-[0-9]{4}-[0-9]{4}/$', views.blocks, name='blocks'),

re_path(r'blocks/[gas|coal|lignite]*[gas|coal|lignite]-*$/', views.blocks, name='blocks'),

re_path(r'blocks/[gas|coal|lignite]*[gas|coal|lignite]-*/', views.blocks, name='blocks'),
    re_path(r'blocks/(gas|coal|lignite)(-)*/[0-9]{4}-[0-9]{4}', views.blocks, name='blocks'),
path('blocks/<int:lower>-<int:upper>', views.blocks, name='blocks'),
'''