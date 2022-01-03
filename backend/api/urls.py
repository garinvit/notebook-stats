from django.urls import path, include
# from rest_framework.routers import DefaultRouter

from .views import AddStatsView

app_name = "api"


urlpatterns = [
    path('stats/', AddStatsView.as_view(), name='stats'),
    path('auth/', include(('garpix_auth.urls', 'garpix_auth'), namespace='garpix_auth')),
]
