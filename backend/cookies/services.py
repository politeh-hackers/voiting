from django.http import HttpResponse


class CookieService:
    def set_cookie(self, response: HttpResponse, key: str, value: str, max_age: int = 10):
        response.set_cookie(key, value, httponly=True, max_age=max_age)

    def get_cookie(self, request, key: str):
        return request.COOKIES.get(key)

    def delete_cookie(self, response: HttpResponse, key: str):
        response.delete_cookie(key)
