from django.urls import path, re_path
from .views import index, pages

urlpatterns = [

    # The home page
    path('', index, name='index'),

    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),

]
