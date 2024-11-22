from idlelib.rpc import request_queue

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from base.service import BaseService
from .models import Category, Appeal, Actual, MediaTag, Admins
from .models import Media
from django.http import HttpRequest, HttpResponse

from .services import MediaService, AppealService, ActualService, CategoryService, AdminsService
import json
import uuid

def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")


def MediaView(View):
    test_service = MediaService(model=Media)

    def get(self, request: HttpRequest):
        return JsonResponse(test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        self.test_service.validation(data)
        self.test_service.create(data)
        return JsonResponse(self.test_service.get_all(), safe=False)

class CategoryView(View):
    test_service = CategoryService(model=Category)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        self.test_service.validation(data)
        self.test_service.create(data)
        return JsonResponse(self.test_service.get_all(), safe=False)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        try:
            self.test_service.delete(model_id=model_id)
            return JsonResponse(self.test_service.get_all(), safe=False, status=204)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid UUID"}, status=400)

    def patch(self, request: HttpRequest, model_id: uuid.UUID):
        try:
            body = json.loads(request.body)
            self.test_service.update(model_id=model_id, data=body)
            return JsonResponse(self.test_service.get_all(), safe=False)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid UUID"}, status=400)

class AdminsView(View):
    test_service = AdminsService(model=Admins)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        self.test_service.validation(data)
        self.test_service.create(data)
        return JsonResponse(self.test_service.get_all(), safe=False)
