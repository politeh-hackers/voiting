from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import BaseUUID


class Admins(BaseUUID):

    
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=100)