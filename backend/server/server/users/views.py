from datetime import timedelta

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.template.defaulttags import now

from users.services import AdminsService
from .models import Admins
import json
from django.views import View
from base.service import BaseValidationService

class Registration(View):
    test_service = AdminsService(model=Admins)

    def save(self, *args, **kwargs):
        if self.remember_me:
            self.expires_at = now() + timedelta(weeks=2)  # 2 недели
        else:
            self.expires_at = now() + timedelta(hours=1)  # 1 час
        super().save(*args, **kwargs)


    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        self.test_service.validation(data)
        self.test_service.create(data)
        return JsonResponse(self.test_service.get_all(), safe=False)

def set(request):
    login = request.GET.get('login')
    password = request.GET.get('password')

