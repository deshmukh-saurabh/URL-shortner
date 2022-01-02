from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("shorten_url/", views.shorten_url, name="shorten_url"),
    path("redirect?<str:redirect_url>", views.redirect, name="redirect")
]