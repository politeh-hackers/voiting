from django.http import JsonResponse, HttpRequest
from pydantic import ValidationError

from users.services import AdminsService
from .models import Admins
import json
from django.views import View
from base.service import BaseValidationService

class Registration(View):
    test_service = AdminsService(model=Admins)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        self.test_service.validation(data)
        self.test_service.create(data)
        return JsonResponse(self.test_service.get_all(), safe=False)



