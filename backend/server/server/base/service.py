from asyncio.windows_events import NULL
from typing import TypeVar, Generic, List, Dict, Protocol
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
import uuid
import re
from django.core.files.images import get_image_dimensions

from .constants import Constants
from .enums import FilterErrorMessages

T = TypeVar("T", bound=models.Model)

MAX_PHOTO_NAME_LENGTH = 255
MAX_PHOTO_SIZE_MB = 5
MAX_PHOTO_SIZE = MAX_PHOTO_SIZE_MB * 1024 * 1024  
MAX_PHOTO_WIDTH = 1920
MAX_PHOTO_HEIGHT = 1080
PASSWORD_MIN_LENGTH = 8
SPECIAL_CHARACTERS = "!@#$%^&*(),.?\":{}|<>"
DATE_FORMAT = "%Y-%m-%d"


class BaseService(Generic[T]):
    model: T

    def __init__(self, model: T):
        self.model = model

    def get_all(self) -> List[dict]:
        return list(self.model.objects.values())

    def create(self, data: Dict) -> None:
        self.model.objects.create(**data)

    def update(self, model_id: uuid.UUID, data: Dict) -> None:
        self.model.objects.filter(id=model_id).update(**data)

    def delete(self, model_id: uuid.UUID) -> None:
        instance: T = self.model.objects.get(id=model_id)
        instance.delete()




class BaseValidationService:

    name_regex = re.compile(r'^[A-Za-zА-Яа-яЁё\s-]+$')  
    phone_regex = re.compile(r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$')  

    @staticmethod
    def validate_presence(value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(FilterErrorMessages.REQUIRED)

    @staticmethod
    def validate_length(field_value: str, min_length: int, max_length: int):
        if field_value and not (min_length <= len(field_value) <= max_length):
            raise ValidationError(FilterErrorMessages.LENGTH)

    @staticmethod
    def validate_name(value: str):
        if value and not BaseValidationService.name_regex.match(value):
            raise ValidationError(FilterErrorMessages.NAME_ERROR)

    @staticmethod
    def validate_phone(value: str):
        if value and not BaseValidationService.phone_regex.match(value):
            raise ValidationError(FilterErrorMessages.NAME_ERROR)

    def validate_common_fields(self, data):
        self.validate_length(data.get('h1'), Constants.MIN_LEN_H1, Constants.MAX_LEN_H1)
        
        self.validate_length(data.get('title'), Constants.MIN_LEN_TITLE, Constants.MAX_LEN_TITLE)
        
        self.validate_length(data.get('description'), Constants.MIN_LEN_DESCRIPTION, Constants.MAX_LEN_DESCRIPTION)
        
        self.validate_presence(data.get('header'))
        self.validate_length(data.get('header'), 1, Constants.MAX_LEN_HEADER)

    def validate_media_actual_fields(self, data):
        self.validate_presence(data.get('main_photo'))

        self.validate_presence(data.get('content'))

        self.validate_length(data.get('content'), Constants.MIN_LEN_TEXT, Constants.MAX_LEN_TEXT)

    def validate_appeal_fields(self, data):
        self.validate_name(data.get('first_name'))

        self.validate_name(data.get('last_name'))

        self.validate_name(data.get('patronymic'))

        self.validate_phone(data.get('phone'))

        self.validate_length(data.get('text'), 500, Constants.MAX_LEN_TEXT)

        self.validate_length(data.get('official_response'), 500, Constants.MAX_LEN_TEXT)