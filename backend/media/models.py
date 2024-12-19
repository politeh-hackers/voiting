from django.db import models
from base.models import BaseUUID

class Media(BaseUUID):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
    header = models.CharField(max_length=200)
    summary = models.CharField(max_length=100, blank=True)
    main_photo = models.TextField(blank=True)
    content = models.JSONField()
    date_created = models.DateField()
    media_tags = models.ManyToManyField("MediaTag", blank=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "media"
        ordering = ['-date_created']


class MediaTag(BaseUUID):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "media tag"
        verbose_name_plural = "media tags"
        ordering = ['name']