from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import BaseUUID


class Admins(AbstractUser):
    username = None  
    login = models.CharField(max_length=150, unique=True)  

    USERNAME_FIELD = 'login'  
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.login