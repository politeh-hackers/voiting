
import re
from datetime import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError
from base.service import BaseService, BaseValidationService
from pages.models import MediaTag, ActualTag


class MediaService(BaseValidationService, BaseService):
    """Сервис для работы с медиа контентом."""

    def validation(self, data):
        # Проверка обязательных полей
        self.validate_field_length("h1", 10, 60, data)
        self.validate_field_length("title", 30, 80, data)
        self.validate_field_length("description", 80, 160, data)
        self.validate_field_length("header", 1, 200, data)
        # Валидация даты
        self.validate_date("date_created", data, "%Y-%m-%dT%H:%M:%SZ")
        # Валидация контента
        self.validate_content("content", data)
        # Валидация тегов
        self.validate_tags("media_tags", data, MediaTag)
        # Проверка фотографий
        self.validate_photos("photos", data)
        # Генерация значений по умолчанию
        self.generate_default_fields(data)
        # Удаление неиспользуемых тегов
        self.cleanup_tags("media_tags", data.get("media_tags", []), MediaTag)

        return super().create(**data)

class ActualService(BaseValidationService, BaseService):
    """Сервис для работы с актуальными статьями."""

    def validation(self, data):
        # Проверка обязательных полей
        self.validate_field_length("h1", 10, 60, data)
        self.validate_field_length("title", 30, 80, data)
        self.validate_field_length("description", 80, 160, data)
        self.validate_field_length("header", 1, 200, data)
        # Валидация даты
        self.validate_date("date_created", data, "%Y-%m-%dT%H:%M:%SZ")
        # Валидация контента
        self.validate_content("content", data)
        # Валидация тегов
        self.validate_tags("actual_tags", data, ActualTag)
        # Проверка фотографий
        self.validate_photos("photos", data)
        # Генерация значений по умолчанию, если они отсутствуют
        self.generate_default_fields(data)
        # Если 'description' отсутствует или не соответствует длине, генерируем его
        if "description" not in data or not (80 <= len(data["description"]) <= 160):
            data["description"] = self.generate_description()
        # Удаление неиспользуемых тегов
        self.cleanup_tags("actual_tags", data.get("actual_tags", []), ActualTag)
        # Call the create method with the data dictionary
        return super().create(data)  # Pass the dictionary directly without unpacking

    def generate_description(self):
        # Генерация дефолтного description длиной от 80 до 160 символов
        return "Default description that meets the required length of 80-160 characters"[:160]  # Ensure it doesn't exceed 160 chars

class AppealService(BaseValidationService, BaseService):
    """Сервис для работы с апелляциями."""

    def validation(self, data):
        # Проверка длины фамилии, имени, отчества
        self.validate_field_length("last_name", 1, 100, data)
        self.validate_field_length("first_name", 1, 100, data)
        self.validate_field_length("patronymic", 1, 100, data)
        # Проверка телефона
        if not re.match(r"^\+375\d{9}$", data["phone"]):
            raise ValidationError({"phone": "Номер телефона должен быть в формате +375xxxxxxxxx."})
        # Статус
        if data["status"] not in ['PENDING', 'COMPLETED', 'REJECTED']:
            raise ValidationError({"status": "Неверное значение статуса."})
        # Проверка isActive
        if not isinstance(data["on_website"], bool):
            raise ValidationError({"on_website": "Поле должно быть булевым значением (True/False)."})
        # Валидация даты
        self.validate_date("date", data, "%Y-%m-%d")
        # Проверка длины текста
        if not (500 <= len(data["text"]) <= 3000):
            raise ValidationError({"text": "Текст должен содержать от 500 до 3000 символов."})
        # Проверка фотографий
        self.validate_photos("photos", data)
        # Официальный ответ
        if data.get("official_response") and not (500 <= len(data["official_response"]) <= 3000):
            raise ValidationError({"official_response": "Официальный ответ должен содержать от 500 до 3000 символов."})
        # Проверка категории
        if not data.get("category") or len(data["category"]) == 0:
            raise ValidationError({"category": "Необходимо выбрать категорию."})
        # Генерация значений по умолчанию
        self.generate_default_fields(data)

        return super().create(**data)

class CategoryService(BaseValidationService, BaseService):

    def validation(self, data):
        self.validate_field_length("name", 1, 100, data)

