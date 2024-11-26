from typing import TypeVar, Generic, List, Dict
from datetime import datetime

from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from base.abstractions import BaseServiceProtocol
from django.db import models
import uuid
import re
from django.core.files.images import get_image_dimensions
from users.models import Admins

T = TypeVar("T", bound=models.Model)

class BaseService(Generic[T]):
    model = T

    def __init__(self, model: T):
        self.model = model

    def get_all(self) -> List[dict]:
        return list(self.model.objects.values())

    def create(self, data: Dict) -> None:
        return self.model.objects.create(**data)

    def update(self, model_id: uuid.UUID, data: dict) -> None:
        return self.model.objects.filter(id=model_id).update(**data)

    def delete(self, model_id: uuid.UUID) -> None:
        instance = self.model.objects.get(id=model_id)
        instance.delete()

class BaseValidationService:
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
        photo = data.get(field_name)

        if photo:
            if not photo.content_type.startswith('image/'):
                raise ValidationError({field_name: "Файл должен быть изображением."})

            if len(photo.name) > 255:
                raise ValidationError({field_name: "Слишком длинное имя файла для фотографии."})

            max_size = 5 * 1024 * 1024  # 5 MB
            if photo.size > max_size:
                raise ValidationError({field_name: "Файл слишком большой. Максимальный размер: 5 МБ."})

            width, height = get_image_dimensions(photo)
            if width > 1920 or height > 1080:
                raise ValidationError({field_name: "Размер изображения должен быть не больше 1920x1080 пикселей."})

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

    def validate_password_strength(self, password, data):
        # Проверка длины пароля
        if len(data[password]) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')

        # Проверка наличия цифры
        if not any(char.isdigit() for char in data[password]):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру.')

        # Проверка наличия специального символа
        special_characters = "!@#$%^&*(),.?\":{}|<>"
        if not any(char in special_characters for char in data[password]):
            raise ValidationError('Пароль должен содержать хотя бы один специальный символ.')

    def validate_login(self, login, data):

        if len(data[login]) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
