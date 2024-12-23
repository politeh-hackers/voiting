from django.http import JsonResponse

class AuthorizationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'DELETE', 'PATCH']:
            if request.path == '/admin/login':  
                return self.get_response(request)

            # user_login = request.COOKIES.get('user_login')
            # if not user_login:
            #     return JsonResponse({"success": False, "message": "Вы не авторизованы."}, status=403)

        return self.get_response(request)
