from django.db import models
from base.models import BaseUUID

class Category(BaseUUID):  # Наследует только от BaseUUID
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"





