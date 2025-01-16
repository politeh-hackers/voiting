from django.db import models
from base.models import BaseUUID

class Media(BaseUUID):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
    header = models.CharField(max_length=200, unique=True, blank=True)
    summary = models.CharField(max_length=100, blank=True, unique=True, null=False)
    main_photo = models.TextField(blank=True, null=False)
    content = models.JSONField(null=False, blank=True)
    date_created = models.DateField(null=False, blank=True)
    media_tags = models.CharField(max_length=100, unique=False)
 
    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "media"
        ordering = ['-date_created']
