from django.urls import path, include, re_path
from .views import *


app_name = "miner"

urlpatterns = [
    path('', index, name='index'),
    path('<int:id>', rig_view, name='rig'),
    # path('stat', stat, name='stat'),
]