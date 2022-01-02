import json
import traceback
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from .helpers import generate_short_url, is_hash_valid


REDIRECT_BASE_URL = "http://{}/redirect/"

def home(request):
    return render(request, 'home.html')


@csrf_exempt
@api_view(["POST"])
def shorten_url(request):
    """
    API view to shorten the URL
    """
    res = {
        "message": "Invalid request!",
        "status": False,
        "data": {}
    }

    # validate request
    try:
        data = request.POST
        print(data)
        original_url = data["original_url"]
        expiration_ts = data["expiration_ts"]
        current_site = get_current_site(request)
    except Exception:
        print(traceback.format_exc())
        return HttpResponse("<h1>Error generating short url!</h1>")

    # shorten the url and return
    try:
        short_url = generate_short_url(original_url, expiration_ts, current_site)
        res["message"] = "Success"
        res["status"] = True
        res["data"]["short_url"] = short_url
        res["data"]["original_url"] = original_url
        return render(request, 'home.html', context=res)
    except Exception:
        print(traceback.format_exc())
        res["message"] = "Error generating short url!"
        return render(request, 'error.html', res)


@api_view(["GET"])
def redirect_to_original_url(request, short_url):
    """
    API view to redirect the user from the short url to the original url
    """
    res = {
        "message": "Invalid request!",
        "status": False,
        "data": {}
    }

    # validate request
    try:
        current_site = get_current_site(request)
        hash = short_url.replace(REDIRECT_BASE_URL.format(current_site), '')
        # check if hash is valid
        valid_hash, original_url = is_hash_valid(hash)
        # if not valid, return error response, else redirec the user to the original url
        if not valid_hash:
            res["message"] = "The page you are looking for does not exist. Either the link is invalid or has expired."
            return render(request, 'error.html', res)
        else:
            return redirect(original_url)
    except Exception:
        print(traceback.format_exc())
        res["message"] = "The page you are looking for does not exist"
        return render(request, 'error.html', res)