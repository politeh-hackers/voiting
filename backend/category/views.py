import json
from .models import Category
from .services import CategoryService
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View

class CategoryView(View):

    test_service = CategoryService(model=Category)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        self.test_service.validate(data)
        self.test_service.create(data)
        return JsonResponse(None, safe=False)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        self.test_service.delete(model_id=model_id)
        return JsonResponse(None, safe=False, status=204)

    def patch(self, request: HttpRequest, model_id: uuid.UUID):
        data = json.loads(request.body)
        self.test_service.validate(data)   
        self.test_service.update(model_id=model_id, data=data)
        return JsonResponse(None, safe=False)
