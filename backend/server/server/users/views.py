from datetime import timedelta

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.template.defaulttags import now

from users.services import AdminsService
from .models import Admins
import json
from django.views import View
from base.service import BaseValidationService

class Login(View):
    
    test_service = AdminsService(model=Admins)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        if self.test_service.authenticate(data['login'], data['password']):
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "message": "Неверный логин или пароль"})

class Registration(View):

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return JsonResponse({"success": False, "message": "Логин и пароль обязательны."})

        if Admins.objects.filter(login=login).exists():
            return JsonResponse({"success": False, "message": "Пользователь с таким логином уже существует."})

        Admins.objects.create(login=login, password=password)
        return JsonResponse({"success": True})


    