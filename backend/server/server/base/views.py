from typing import TypeVar, Generic
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models


T = TypeVar("T", bound=models.Model)

class BaseView(Generic[T], APIView):
    model = T

    def get_queryset(self):
        return self.model.objects.get_queryset()



