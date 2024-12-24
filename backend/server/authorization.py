from django.http import JsonResponse
from cookies.services import CookieService
from django.core.handlers.wsgi import WSGIRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

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

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/admin/login':
            return self.get_response(request)

        if request.method in ['POST', 'GET', 'PATCH', 'DELETE']:
            auth_header = request.headers.get('Authorization')

            if auth_header:
                try:
                    token = auth_header.split()[1] 
                    AccessToken(token) 
                except (IndexError, ValueError, TokenError):
                    return JsonResponse("Error")

        return self.get_response(request)