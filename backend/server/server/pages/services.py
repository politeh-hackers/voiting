from typing import List
import re
from datetime import datetime
from django.core.exceptions import ValidationError
from base.service import BaseService


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
    def validation(self, data): ...

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

