import os
from idlelib.rpc import request_queue
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from base.service import BaseService
from .models import Category, Appeal, Actual, MediaTag
from .models import Media
from django.http import HttpRequest, HttpResponse
from static import images
from .services import MediaService, AppealService, ActualService, CategoryService
import json
import uuid

def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")

import json
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
from .models import Media
from .services import MediaService  # Предположим, что у вас есть MediaService

class MediaView(View):
    test_service = MediaService(model=Media)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)

        image_path = os.path.join('images', data['content'])
        with open(image_path, 'wb') as image_file:
            image_file.write(data['content'])


        self.test_service.create(data)


        return JsonResponse(None, safe=False)

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

class ActualView(View):
    test_service = ActualService(model=Actual)

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

class AppealView(View):
    test_service = AppealService(model=Appeal)

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

class CategoryView(View):
    test_service = CategoryService(model=Category)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        try:
            data = json.loads(request.body)
            self.test_service.validation(data)
            self.test_service.create(data)
            return JsonResponse(None, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

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
