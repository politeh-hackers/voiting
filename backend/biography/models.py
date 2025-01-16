from django.db import models
from base.models import BaseUUID

class Biography(BaseUUID):
    h1 = models.CharField(max_length=60, blank=True, unique=True)
    title = models.CharField(max_length=80, blank=True, unique=True)
    description = models.CharField(max_length=160, blank=True, unique=True)
    header = models.CharField(max_length=200, null=False, blank=True)
    main_photo = models.TextField(blank=True, null=False)
    content = models.JSONField(null=False)
    date = models.DateField(null=False, blank=True)

    class Meta:
        verbose_name = "biography"
        verbose_name_plural = "biography"