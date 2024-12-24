from django.http import JsonResponse, HttpRequest
from users.services import AdminsService
from .models import Admins
import json
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from cookies.services import CookieService

class Login(View):
    cookie_service = CookieService()
    def post(self, request):
        data = json.loads(request.body)
        login = data.get('login')
        password = data.get('password')
        if not login or not password:
            return JsonResponse({"success": False, "message": "Логин и пароль обязательны."})
        try:
            admin = Admins.objects.get(login=login)
        except Admins.DoesNotExist:
            return JsonResponse({"success": False, "message": "Неверный логин или пароль"})
        if check_password(password, admin.password):
            response = JsonResponse({"success": True, "message": "Вход выполнен"})
            self.cookie_service.set_cookie(response, 'user_login', login, 3600)
            return response
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
        hashed_password = make_password(password)
        Admins.objects.create(login=login, password=hashed_password)
        return JsonResponse({"success": True})

class Logout(View):
    cookie_service = CookieService()
    def post(self, request: HttpRequest):
        response = JsonResponse({"success": True, "message": "Вы вышли из системы"})
        self.cookie_service.delete_cookie(response, 'user_login')
        return response

