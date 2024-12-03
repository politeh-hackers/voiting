import os
from django.core.handlers.wsgi import WSGIRequest
from .models import Category, Appeal, Actual, Media
from .services import MediaService, AppealService, ActualService, CategoryService
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
import json

class MediaView(View):
    test_service = MediaService(model=Media)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request):
        data = request.POST.dict()
        self.test_service.create(data)
        return JsonResponse(self.test_service.get_all(), safe=False)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        try:
            self.test_service.delete(model_id=model_id)
            return JsonResponse(self.test_service.get_all(), safe=False, status=204)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid UUID"}, status=400)


class ImageView(View):
    test_service = MediaService(model=Media)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: WSGIRequest):
        data = request.FILES["image"]
        data_str = str(data)
        image_path = os.path.join('static/images', data_str)
        with open(image_path, 'wb') as image_file:
            for chunk in data.chunks():
                image_file.write(chunk)
        return JsonResponse(
            {
                "url": f"http://localhost:8000/static/images/{data_str}",
                "name": data_str,
                "size": data.size,
                "type": data.content_type
            }, safe=False)

    def delete(self, request: HttpRequest, file_name: str):
        try:
            # Генерация полного пути к файлу
            image_path = os.path.join('static/images', file_name)

            # Проверка существования файла
            if os.path.exists(image_path):
                os.remove(image_path)  # Удаление файла
                return JsonResponse({"message": f"File {file_name} deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": f"File {file_name} not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    # def delete(self, request: HttpRequest, model_id: uuid.UUID):
    #     try:
    #         self.test_service.delete(model_id=model_id)
    #         return JsonResponse(self.test_service.get_all(), safe=False, status=204)
    #     except (ValueError, TypeError):
    #         return JsonResponse({"error": "Invalid UUID"}, status=400)
    #
    # def patch(self, request: HttpRequest, model_id: uuid.UUID):
    #     try:
    #         body = json.loads(request.body)
    #         self.test_service.update(model_id=model_id, data=body)
    #         return JsonResponse(self.test_service.get_all(), safe=False)
    #     except (ValueError, TypeError):
    #         return JsonResponse({"error": "Invalid UUID"}, status=400)

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
