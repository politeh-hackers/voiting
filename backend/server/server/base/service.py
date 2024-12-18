from asyncio.windows_events import NULL
from typing import TypeVar, Generic, List, Dict, Protocol
from datetime import date, datetime
from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.db import models
import uuid
import re
from django.core.files.images import get_image_dimensions
from .constants import Constants
from .enums import FilterErrorMessages

T = TypeVar("T", bound=models.Model)


class BaseService(Generic[T]):
    
    model: T

    def __init__(self, model: T):
        self.model = model

    def get_all(self) -> List[dict]:
        return list(self.model.objects.values())

    def create(self, data: T) -> None:
        self.model.objects.create(**data)

    def update(self, model_id: uuid.UUID, data: Dict) -> None:
        self.model.objects.filter(id=model_id).update(**data)

    def delete(self, model_id: uuid.UUID) -> None:
        instance: T = self.model.objects.get(id=model_id)
        instance.delete()








# class BaseValidationService:

#     name_regex = re.compile(r'^[A-Za-zА-Яа-яЁё\s-]+$')  
#     phone_regex = re.compile(r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$')  


#     def validate_appeal_fields(self, data):

#         self.validate_phone(data.get('phone'))


#         self.validate_length(data.get('official_response'), 500, Constants.MAX_LEN_TEXT)