from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Media


def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")

def media(request):
    pass


def biography(request):
    return JsonResponse({"gh": "хуй"})

def appeals(request):
    return HttpResponse("<h1>ЖОПА</h1>")