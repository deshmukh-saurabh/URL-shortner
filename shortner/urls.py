from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("shorten_url", views.shorten_url, name="shorten_url"),
    path("redirect/<str:short_url>", views.redirect_to_original_url, name="redirect_to_original_url")
]