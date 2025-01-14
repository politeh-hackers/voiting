from django.db import Error
from django.http import JsonResponse
from rest_framework_simplejwt.settings import api_settings
import jwt


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
<<<<<<< HEAD
        exeption_paths = ['/admin/login', '/appeals/appeals', '/appeals/', '/admin/image']
=======
        exeption_paths = ['/admin/login', '/appeals/appeals', '/appeals/', '/admin/image', '/gpt/generate']
>>>>>>> 504da75ece884c7a1396b427f009179a62c1e607
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