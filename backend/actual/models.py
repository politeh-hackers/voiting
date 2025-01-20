from django.db import models
from base.models import BaseUUID
from django.utils import timezone

class Actual(BaseUUID): 
    h1 = models.CharField(max_length=60, blank=True, unique=False)
    title = models.CharField(max_length=80, blank=True, unique=False)
    description = models.CharField(max_length=160, blank=True, unique=False)
    header = models.CharField(max_length=200, unique=True, null=False)
    summary = models.CharField(max_length=100, blank=True, unique=True, null=False)
    main_photo = models.TextField(blank=True, null=False)
    content = models.JSONField(null=False)
    date_created = models.DateTimeField(null=False)
    actual_tags = models.CharField(max_length=100, unique=False)

    class Meta:
        verbose_name = "actual"
        verbose_name_plural = "actual"
        ordering = ['-date_created']
