from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Category
from .models import Media
from django.http import HttpRequest, HttpResponse

from .services import AppealService, TestService
import json


def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")

def media(request):
    pass

def test(request: HttpRequest):
    appeal_service = TestService(model=Category)
    if request.method == "GET":
        return JsonResponse(appeal_service.get_all(), safe=False)
    if request.method == "POST":
         data = json.loads(request.body)
         appeal_service.create(data)
         return JsonResponse(appeal_service.get_all(), safe=False)

