from django.contrib.auth.models import AbstractUser
from django.db import models
from pages.models import BaseUUID


class Admins(BaseUUID):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    remember_me = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()