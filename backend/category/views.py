import json
from .models import Category
from .services import CategoryService
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
from cookies.services import CookieService
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

class CategoryView(View):

    test_service = CategoryService(model=Category)

    def get(self, request: HttpRequest):
        # Проверка на наличие токена в заголовке Authorization
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse({"success": False, "message": "Отсутствует токен авторизации."}, status=401)

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return JsonResponse({"success": False, "message": "Неверный формат токена."}, status=401)
            
            token = parts[1]  # Это сам токен
            # Проверяем валидность токена
            AccessToken(token)  # Если токен невалидный или просроченный, выбросится ошибка
        except (IndexError, TokenError):
            return JsonResponse({"success": False, "message": "Неверный или просроченный токен."}, status=401)

        # Если токен валиден, выполняем дальнейшую обработку
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
