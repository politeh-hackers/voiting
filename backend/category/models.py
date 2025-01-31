from django.db import models
from base.models import BaseUUID
import uuid

class Category(models.Model): 
    name = models.CharField(max_length=100, unique=True, blank=True, null=False)

    def __str__(self):
        return self.name






