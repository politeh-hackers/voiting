from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from base.service import BaseService
from .models import Category, Appeal, Actual
from .models import Media
from django.http import HttpRequest, HttpResponse

from .services import MediaService, AppealService, ActualService
import json


def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")


def test(request: HttpRequest):
    test_service = ActualService(model=Actual)
    if request.method == "GET":
        return JsonResponse(test_service.get_all(), safe=False)
    if request.method == "POST":
         data = json.loads(request.body)
         test_service.validation(data)
         test_service.create(data)
         return JsonResponse(test_service.get_all(), safe=False)

