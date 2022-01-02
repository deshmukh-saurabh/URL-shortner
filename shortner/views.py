from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>URL shortner</h1>")

@api_view(["POST"])
def shorten_url(request):
    """
    API view to shorten the URL
    """
    pass


@api_view(["GET"])
def redirect(request):
    """
    API view to redirect the user from the short url to the original url
    """
    pass