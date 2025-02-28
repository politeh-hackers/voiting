from django.db import Error
from django.http import JsonResponse
from rest_framework_simplejwt.settings import api_settings
import jwt


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exeption_paths = ['/admin/login', '/admin/registration', '/appeals/appeals/', '/appeals/', '/admin/image']
        if request.method in ['POST', 'PATCH', 'DELETE'] and request.path not in exeption_paths:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({"success": False, "message": "Authorization token is missing."}, status=401)
            try:
                jwt.decode(
                    token,
                    api_settings.SIGNING_KEY,
                    algorithms=[api_settings.ALGORITHM]
                )
            except Error as e:
                return JsonResponse({"success": False, "message": str(e)}, status=401)
        return self.get_response(request)