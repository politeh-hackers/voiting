from django.http import JsonResponse
from cookies.services import CookieService
from django.core.handlers.wsgi import WSGIRequest
from rest_framework_simplejwt.authentication import JWTAuthentication

# class AuthorizationMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.cookie_service = CookieService()

#     def __call__(self, request: WSGIRequest):
#         methods_requiring_auth = ['GET', 'POST', 'DELETE', 'PATCH']

#         if request.method in methods_requiring_auth:
#             if request.path == '/admin/login':  
#                 return self.get_response(request)

#             user_login = self.cookie_service.get_cookie(request, 'user_login')
#             print(request.COOKIES)
#             print("юзер логин:", user_login)

#             if not user_login:
#                 return JsonResponse({"success": False, "message": "Вы не авторизованы."}, status=403)

#         return self.get_response(request)

class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request: WSGIRequest):
        methods_requiring_auth = ['GET', 'POST', 'DELETE', 'PATCH']

        if request.method in methods_requiring_auth:
            if request.path == '/admin/login':  # Исключение для страницы логина
                return self.get_response(request)

            # Проверяем JWT токен
            try:
                user, token = self.jwt_authenticator.authenticate(request)
                if user is not None:
                    request.user = user  # Ассоциируем пользователя с запросом
                else:
                    return JsonResponse({"success": False, "message": "Вы не авторизованы."}, status=403)
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=403)

        return self.get_response(request)