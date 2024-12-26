from django.http import JsonResponse, HttpRequest
from users.services import AdminsService
from .models import Admins
import json
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class Login(APIView):
    
    def post(self, request):
        data = request.data
        login = data.get('login')
        password = data.get('password')
        if not login or not password:
            return Response({"success": False, "message": "Логин и пароль обязательны."}, status=400)
        user = authenticate(request, username=login, password=password)
        if user is None:
            return Response({"success": False, "message": "Неверный логин или пароль."}, status=401)
        refresh = RefreshToken.for_user(user)
        access_token = RefreshToken.access_token
        return Response({
            "access": str(access_token), 
            "refresh": str(refresh),      
        })
 
class Logout(View):
    def post(self, request: HttpRequest):
        response = JsonResponse({"success": True, "message": "Вы вышли из системы"})
        return response

class Registration(APIView):

    def post(self, request):
        data = request.data
        login = data.get('login')
        password = data.get('password')
        if not login or not password:
            return Response({"success": False, "message": "Логин и пароль обязательны."}, status=400)
        User = get_user_model()
        if User.objects.filter(login=login).exists():
            return Response({"success": False, "message": "Пользователь с таким логином уже существует."}, status=400)
        user = User.objects.create(
            login=login,
            password=make_password(password)  
        )
        refresh = RefreshToken.for_user(user)
        access_token = RefreshToken.access_token
        return Response({
            "success": True,
            "message": "Пользователь зарегистрирован.",
            "access": str(access_token),
            "refresh": str(refresh),
        })