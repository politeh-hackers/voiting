from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import BaseUUID


class Admins(AbstractUser):
    login = models.CharField(max_length=150, unique=True)  # Используем login вместо username

    USERNAME_FIELD = 'login'  # Поле, используемое для аутентификации
    REQUIRED_FIELDS = []      # Поля, обязательные для заполнения при создании пользователя

    def __str__(self):
        return self.login