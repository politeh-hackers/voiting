from typing import List
import re
from datetime import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError
from base.service import BaseService
from pages.models import MediaTag, ActualTag


class TestService(BaseService):
    def get_all(self) -> List:
        all_res = super().get_all()
        all_res.append({"asd": "asdasd"})
        return all_res

class BasicService(BaseService):

    def validation(self, data):

        # Проверка длины поля h1 (от 10 до 60 символов)
        if "h1" in data:
            if not (10 <= len(data["h1"]) <= 60):
                raise ValidationError({"h1": "Поле 'h1' должно содержать от 10 до 60 символов."})
        else:
            raise ValidationError({"h1": "Поле 'h1' обязательно."})

        # Проверка длины поля title (от 30 до 80 символов)
        if "title" in data:
            if not (30 <= len(data["title"]) <= 80):
                raise ValidationError({"title": "Поле 'title' должно содержать от 30 до 80 символов."})
        else:
            raise ValidationError({"title": "Поле 'title' обязательно."})

        # Проверка длины поля description (от 80 до 160 символов)
        if "description" in data:
            if not (80 <= len(data["description"]) <= 160):
                raise ValidationError(
                    {"description": "Поле 'description' должно содержать от 80 до 160 символов."})
        else:
            raise ValidationError({"description": "Поле 'description' обязательно."})

        # Генерация значений для полей, если они не указаны
        if not data.get("h1"):
            data["h1"] = self.generate_h1()
        if not data.get("title"):
            data["title"] = self.generate_title()
        if not data.get("description"):
            data["description"] = self.generate_description()

        # Валидация дополнительных полей, если они существуют
        if data.get("category") and len(data["category"]) == 0:
            raise ValidationError({"category": "Необходимо выбрать категорию."})

        super().create(**data)

    def generate_h1(self):
        return "H1"

    def generate_title(self):
        return "Title"

    def generate_description(self):
        return "Description"

class MediaService(BaseService):

    def validation(self, data):

        # Валидация h1 (от 10 до 60 символов)
        if "h1" not in data or not (10 <= len(data["h1"]) <= 60):
            raise ValidationError({"h1": "Поле 'h1' должно содержать от 10 до 60 символов."})

        # Валидация title (от 30 до 80 символов)
        if "title" not in data or not (30 <= len(data["title"]) <= 80):
            raise ValidationError({"title": "Поле 'title' должно содержать от 30 до 80 символов."})

        # Валидация description (от 80 до 160 символов)
        if "description" not in data or not (80 <= len(data["description"]) <= 160):
            raise ValidationError({"description": "Поле 'description' должно содержать от 80 до 160 символов."})

        # Валидация header (до 200 символов)
        if "header" not in data or not (1 <= len(data["header"]) <= 200):
            raise ValidationError({"header": "Поле 'header' обязательно и должно содержать не более 200 символов."})

        # Проверка фотографий (если они указаны)
        if data.get("photos") and len(data["photos"]) > 255:
            raise ValidationError({"photos": "Слишком длинное имя файла для фотографии."})

        # Валидация даты (по умолчанию текущая)
        if "date_created" in data:
            try:
                datetime.strptime(data["date_created"], "%Y-%m-%d")
            except ValueError:
                raise ValidationError({"date_created": "Дата должна быть в формате YYYY-MM-DD."})
        else:
            data["date_created"] = timezone.now()

        # Валидация контента
        if "content" not in data or not data["content"].strip():
            raise ValidationError({"content": "Поле 'content' обязательно."})

        # Валидация тегов
        if "media_tags" in data:
            media_tags = data["media_tags"]
            if not isinstance(media_tags, list):
                raise ValidationError({"media_tags": "Теги должны быть в виде списка."})
            # Проверка, существуют ли теги в базе
            existing_tags = set(MediaTag.objects.filter(name__in=media_tags).values_list("name", flat=True))
            invalid_tags = set(media_tags) - existing_tags
            if invalid_tags:
                raise ValidationError({"media_tags": f"Неверные теги: {', '.join(invalid_tags)}"})

        # Удаление тегов при удалении статьи или уникального тега
        self.cleanup_tags(data.get("media_tags", []))

        # Генерация значений, если их нет
        data.setdefault("h1", self.generate_h1())
        data.setdefault("title", self.generate_title())
        data.setdefault("description", self.generate_description())

        # Сохранение статьи
        return super().create(**data)

    def cleanup_tags(self, tags):
        """Удаление тегов, если они больше не используются."""
        for tag_name in tags:
            tag = MediaTag.objects.filter(name=tag_name).first()
            if tag and not tag.media_set.exists():  # Если тег больше нигде не используется
                tag.delete()

    def generate_h1(self):
        return "Default H1"

    def generate_title(self):
        return "Default Title"

    def generate_description(self):
        return "Default Description"

class ActualService(BaseService):

    def validation(self, data):

        # Валидация h1 (от 10 до 60 символов)
        if "h1" not in data or not (10 <= len(data["h1"]) <= 60):
            raise ValidationError({"h1": "Поле 'h1' должно содержать от 10 до 60 символов."})

        # Валидация title (от 30 до 80 символов)
        if "title" not in data or not (30 <= len(data["title"]) <= 80):
            raise ValidationError({"title": "Поле 'title' должно содержать от 30 до 80 символов."})

        # Валидация description (от 80 до 160 символов)
        if "description" not in data or not (10 <= len(data["description"]) <= 160):
            raise ValidationError({"description": "Поле 'description' должно содержать от 80 до 160 символов."})

        # Валидация header (до 200 символов)
        if "header" not in data or not (1 <= len(data["header"]) <= 200):
            raise ValidationError({"header": "Поле 'header' обязательно и должно содержать не более 200 символов."})

        # Проверка фотографий (если они указаны)
        if data.get("photos") and len(data["photos"]) > 255:
            raise ValidationError({"photos": "Слишком длинное имя файла для фотографии."})

        # Валидация даты (по умолчанию текущая)
        if "date_created" in data:
            try:
                datetime.strptime(data["date_created"], "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                raise ValidationError({"date_created": "Дата должна быть в формате YYYY-MM-DD."})
        else:
            data["date_created"] = timezone.now()

        # Валидация контента
        if "content" not in data or not data["content"].strip():
            raise ValidationError({"content": "Поле 'content' обязательно."})

        # Валидация тегов
        if "actual_tags" in data:
            actual_tags = data["actual_tags"]
            if not isinstance(actual_tags, list):
                raise ValidationError({"actual_tags": "Теги должны быть в виде списка."})
            # Проверка, существуют ли теги в базе
            existing_tags = set(ActualTag.objects.filter(name__in=actual_tags).values_list("name", flat=True))
            invalid_tags = set(actual_tags) - existing_tags
            if invalid_tags:
                raise ValidationError({"actual_tags": f"Неверные теги: {', '.join(invalid_tags)}"})

        # Удаление тегов при удалении статьи или уникального тега
        self.cleanup_tags(data.get("actual_tags", []))

        # Генерация значений, если их нет
        data.setdefault("h1", self.generate_h1())
        data.setdefault("title", self.generate_title())
        data.setdefault("description", self.generate_description())

        # Сохранение статьи
        def create(self, data):
            # Сначала выполняем валидацию
            self.validation(data)
            # После этого сохраняем данные
            return super().create(**data)

    def cleanup_tags(self, tags):
        """Удаление тегов, если они больше не используются."""
        for tag_name in tags:
            tag = ActualTag.objects.filter(name=tag_name).first()
            if tag and not tag.actual.exists():  # Если тег больше нигде не используется
                tag.delete()

    def generate_h1(self):
        return "Default H1"

    def generate_title(self):
        return "Default Title"

    def generate_description(self):
        return "Default Description"

class AppealService(BaseService):
    def validation(self, data):

        # Проверка длины фамилии, имени, отчества (макс. 100 символов)
        if not (1 <= len(data["last_name"]) <= 100):
            raise ValidationError({"last_name": "Фамилия должна содержать от 1 до 100 символов."})
        if not (1 <= len(data["first_name"]) <= 100):
            raise ValidationError({"first_name": "Имя должно содержать от 1 до 100 символов."})
        if not (1 <= len(data["patronymic"]) <= 100):
            raise ValidationError({"patronymic": "Отчество должно содержать от 1 до 100 символов."})

        # Проверка корректности номера телефона (в формате +375)
        if not re.match(r"^\+375\d{9}$", data["phone"]):
            raise ValidationError({"phone": "Номер телефона должен быть в формате +375xxxxxxxxx."})

        # Проверка наличия статуса из разрешенных значений
        if data["status"] not in ['PENDING', 'COMPLETED', 'REJECTED']:
            raise ValidationError({"status": "Неверное значение статуса."})

        # Проверка того, что поле "isActive" (on_website) имеет логическое значение
        if not isinstance(data["on_website"], bool):
            raise ValidationError({"on_website": "Поле должно быть булевым значением (True/False)."})

        # Проверка даты
        try:
            datetime.strptime(data["date"], "%Y-%m-%d")
        except ValueError:
            raise ValidationError({"date": "Дата должна быть в формате YYYY-MM-DD."})

        # Проверка длины текста
        if not (500 <= len(data["text"]) <= 3000):
            raise ValidationError({"text": "Текст должен содержать от 500 до 3000 символов."})

        # Проверка фотографий (если они указаны)
        if data.get("photos") and len(data["photos"]) > 255:
            raise ValidationError({"photos": "Слишком длинное имя файла для фотографии."})

        # Проверка официального ответа (если указан)
        if data.get("official_response") and not (500 <= len(data["official_response"]) <= 3000):
            raise ValidationError({"official_response": "Официальный ответ должен содержать от 500 до 3000 символов."})

        # Проверка наличия хотя бы одной категории
        if not data.get("category") or len(data["category"]) == 0:
            raise ValidationError({"category": "Необходимо выбрать категорию."})

        # Если все проверки прошли успешно, вызываем создание
        super().create(**data)