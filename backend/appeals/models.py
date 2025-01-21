from django.db import models
from base.models import BaseUUID
from django.utils import timezone

class Appeal(BaseUUID):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
    header = models.CharField(max_length=200, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    first_name = models.CharField(max_length=100, null=False, blank=True)
    patronymic = models.CharField(max_length=100, null=False, blank=True)
    phone = models.CharField(max_length=100, null=False, blank=True)
    location = models.CharField(max_length=255, blank=True, null=False)
    status = models.CharField(max_length=10, null=False, blank=True)
    on_website = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now, null=False, blank=True)
    text = models.CharField(max_length=200, null=False, blank=True)
    photos = models.CharField(max_length=255, null=True, blank=True)
    official_response = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=200, blank=True, null=False)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Appeals"
        verbose_name = "Appeal"
