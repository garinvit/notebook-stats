from django.urls import path
from .views import login_view, register_user  # logout_view
from django.contrib.auth.views import LogoutView, logout_then_login

app_name = "auth"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_then_login, name="logout")
]
