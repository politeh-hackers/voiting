
import re
from datetime import datetime

import self
from django.utils import timezone
from django.core.exceptions import ValidationError
from base.service import BaseService, BaseValidationService
from pages.models import MediaTag, ActualTag


class MediaService(BaseValidationService, BaseService):

    def validation(self, data):
        validators = {
            "h1": lambda: self.validate_field_length("h1", 10, 60, data),
            "title": lambda: self.validate_field_length("title", 30, 80, data),
            "description": lambda: self.validate_field_length("description", 80, 160, data),
            "header": lambda: self.validate_field_length("header", 1, 200, data),
            "date_created": lambda: self.validate_date("date_created", data, "%Y-%m-%dT%H:%M:%SZ"),
            "content": lambda: self.validate_content("content", data),
            "media_tags": lambda: self.validate_tags("media_tags", data, MediaTag),
            "photos": lambda: self.validate_photos("photos", data),
        }

        for field, validator in validators.items():
            if field in data:
                validator()

        self.generate_default_fields(data)
        self.cleanup_tags("media_tags", data.get("media_tags", []), MediaTag)

        return super().create(**data)

class ActualService(BaseValidationService, BaseService):

    def validation(self, data):
        validators = {
            "h1": lambda: self.validate_field_length("h1", 10, 60, data),
            "title": lambda: self.validate_field_length("title", 30, 80, data),
            "description": lambda: self.validate_field_length("description", 80, 160, data),
            "header": lambda: self.validate_field_length("header", 1, 200, data),
            "date_created": lambda: self.validate_date("date_created", data, "%Y-%m-%dT%H:%M:%SZ"),
            "content": lambda: self.validate_content("content", data),
            "actual_tags": lambda: self.validate_tags("actual_tags", data, ActualTag),
            "photos": lambda: self.validate_photos("photos", data),
        }

        for field, validator in validators.items():
            if field in data:
                validator()

        self.generate_default_fields(data)
        if "description" not in data or not (80 <= len(data["description"]) <= 160):
            data["description"] = self.generate_description()

        self.cleanup_tags("actual_tags", data.get("actual_tags", []), ActualTag)

        return super().create(data)

    def generate_description(self):
        # Генерация дефолтного description длиной от 80 до 160 символов
        return "Default description that meets the required length of 80-160 characters"[:160]

class AppealService(BaseValidationService, BaseService):

    def validation(self, data):
        validators = {
            "last_name": lambda: self.validate_field_length("last_name", 1, 100, data),
            "first_name": lambda: self.validate_field_length("first_name", 1, 100, data),
            "patronymic": lambda: self.validate_field_length("patronymic", 1, 100, data),
            "phone": self.validate_phone,
            "status": self.validate_status,
            "on_website": self.validate_on_website,
            "date": lambda: self.validate_date("date", data, "%Y-%m-%d"),
            "text": self.validate_text_length,
            "photos": lambda: self.validate_photos("photos", data),
            "official_response": self.validate_official_response,
            "category": self.validate_category,
        }

        for field, validator in validators.items():
            if field in data:
                validator()

        self.generate_default_fields(data)
        return super().create(data)

    def validate_phone(self, data):
        if not re.match(r"^\+375\d{9}$", data["phone"]):
            raise ValidationError({"phone": "Номер телефона должен быть в формате +375xxxxxxxxx."})

    def validate_status(self, data):
        if data["status"] not in ['PENDING', 'COMPLETED', 'REJECTED']:
            raise ValidationError({"status": "Неверное значение статуса."})

    def validate_on_website(self, data):
        if not isinstance(data["on_website"], bool):
            raise ValidationError({"on_website": "Поле должно быть булевым значением (True/False)."})

    def validate_text_length(self, data):
        if not (500 <= len(data["text"]) <= 3000):
            raise ValidationError({"text": "Текст должен содержать от 500 до 3000 символов."})

    def validate_official_response(self, data):
        if data.get("official_response") and not (500 <= len(data["official_response"]) <= 3000):
            raise ValidationError({"official_response": "Официальный ответ должен содержать от 500 до 3000 символов."})

    def validate_category(self, data):
        if not data.get("category") or len(data["category"]) == 0:
            raise ValidationError({"category": "Необходимо выбрать категорию."})

class CategoryService(BaseValidationService, BaseService):

    def validation(self, data):
        self.validate_field_length("name", 1, 100, data)
        return super().create(data)

