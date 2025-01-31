from django.db import models
from category.models import Category
from base.models import BaseUUID
from django.utils import timezone
import uuid

class Appeal(models.Model):
    slug = models.SlugField(unique=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    h1 = models.CharField(max_length=60, null=True, blank=True)
    title = models.CharField(max_length=80, null=True, blank=True)
    description = models.CharField(max_length=160, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    location = models.JSONField(max_length=255, null=True, blank=True, )
    status = models.CharField(max_length=10, null=True, blank=True)
    on_website = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)
    text = models.CharField(max_length=200, null=True, blank=True)
    photos = models.CharField(max_length=200, null=True, blank=True)
    official_response = models.JSONField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)

    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Appeals"
        verbose_name = "Appeal"
