
import re
from datetime import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError
from base.service import BaseService
from pages.models import MediaTag, ActualTag


class BaseValidationService(BaseService):
    """Базовый сервис для общей валидации."""

    def validate_field_length(self, field_name, min_length, max_length, data):
        """Проверка длины строкового поля."""
        if field_name in data:
            if not (min_length <= len(data[field_name]) <= max_length):
                raise ValidationError(
                    {field_name: f"Поле '{field_name}' должно содержать от {min_length} до {max_length} символов."})
        else:
            raise ValidationError({field_name: f"Поле '{field_name}' обязательно."})

    def validate_date(self, field_name, data, date_format="%Y-%m-%d"):
        """Проверка правильности формата даты."""
        if field_name in data:
            try:
                datetime.strptime(data[field_name], date_format)
            except ValueError:
                raise ValidationError({field_name: f"Дата должна быть в формате {date_format}."})
        else:
            data[field_name] = timezone.now()

    def validate_tags(self, field_name, data, tag_model):
        """Проверка правильности тегов."""
        if field_name in data:
            tags = data[field_name]
            if not isinstance(tags, list):
                raise ValidationError({field_name: "Теги должны быть в виде списка."})
            # Проверка, существуют ли теги в базе
            existing_tags = set(tag_model.objects.filter(name__in=tags).values_list("name", flat=True))
            invalid_tags = set(tags) - existing_tags
            if invalid_tags:
                raise ValidationError({field_name: f"Неверные теги: {', '.join(invalid_tags)}"})

    def validate_content(self, field_name, data):
        """Проверка наличия контента."""
        if field_name not in data or not data[field_name].strip():
            raise ValidationError({field_name: "Поле 'content' обязательно."})

    def validate_photos(self, field_name, data):
        """Проверка фотографий (если они указаны)."""
        if data.get(field_name) and len(data[field_name]) > 255:
            raise ValidationError({field_name: "Слишком длинное имя файла для фотографии."})

    def generate_default_fields(self, data):
        """Генерация значений по умолчанию для полей, если они не указаны."""
        data.setdefault("h1", self.generate_h1())
        data.setdefault("title", self.generate_title())
        data.setdefault("description", self.generate_description())

    def cleanup_tags(self, field_name, tags, tag_model):
        """Удаление тегов, если они больше не используются."""
        for tag_name in tags:
            tag = tag_model.objects.filter(name=tag_name).first()
            if tag and not tag.__getattr__(
                    tag_model._meta.model_name).exists():  # Проверка, если тег больше нигде не используется
                tag.delete()

    def generate_h1(self):
        return "Default H1"

    def generate_title(self):
        return "Default Title"

    def generate_description(self):
        return "Default Description"

class MediaService(BaseValidationService):
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

class ActualService(BaseValidationService):
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

class AppealService(BaseValidationService):
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

class CategoryService(BaseValidationService):

    def validation(self, data):
        self.validate_field_length("category", 1, 100, data)

