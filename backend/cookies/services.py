from django.http import HttpResponse


class CookieService:
    
    def set_cookie(self, response: HttpResponse, key: str, value: str, max_age: int):
        print(f"юзерс: {key}={value}")
        response.set_cookie(key, value, max_age=max_age, domain="localhost:5173")


    def get_cookie(self, request, key: str):
        return request.COOKIES.get(key)

    def delete_cookie(self, response: HttpResponse, key: str):
        response.delete_cookie(key)
