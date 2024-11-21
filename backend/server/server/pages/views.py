from idlelib.rpc import request_queue

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from base.service import BaseService
from .models import Category, Appeal, Actual, MediaTag
from .models import Media
from django.http import HttpRequest, HttpResponse

from .services import MediaService, AppealService, ActualService, CategoryService
import json


def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")

def admin(request):
    return HttpResponse("<h1>Admin</h1>")

def MediaView(request: HttpRequest):
    test_service = MediaService(model=Media)
    if request.method == "GET":
        return JsonResponse(test_service.get_all(), safe=False)
    if request.method == "POST":
         data = json.loads(request.body)
         test_service.validation(data)
         test_service.create(data)
         return JsonResponse(test_service.get_all(), safe=False)
    # if request.method == "DELETE":
    #      body = json.loads(request.body)
    #      test_id = body.get("id")
    #      test_service.delete(model_id=int(test_id))
    #      return JsonResponse(test_service.get_all(), safe=False)
    # if request.method == "PATCH":
    #     body = json.loads(request.body)
    #     test_id = body.get("id")
    #     test_service.update(model_id=int(test_id), data=body)
    #     return JsonResponse(test_service.get_all(), safe=False)

def CategoryView(request: HttpRequest):
    test_service = CategoryService(model=Category)
    if request.method == "GET":
        return JsonResponse(test_service.get_all(), safe=False)
    if request.method == "POST":
        data = json.loads(request.body)
        test_service.validation(data)
        test_service.create(data)
        return JsonResponse(test_service.get_all(), safe=False)
    if request.method == "DELETE":
        body = json.loads(request.body)
        test_id = body.get("id")
        test_service.delete(model_id=int(test_id))
        return JsonResponse(test_service.get_all(), safe=False)
    if request.method == "PATCH":
        body = json.loads(request.body)
        test_id = body.get("id")
        test_service.update(model_id=int(test_id), data=body)
        return JsonResponse(test_service.get_all(), safe=False)