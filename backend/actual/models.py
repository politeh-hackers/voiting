from django.db import models
from base.models import BaseUUID
from django.utils import timezone

class Actual(BaseUUID): 
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
    header = models.CharField(max_length=200)
    summary = models.CharField(max_length=100, blank=True)
    main_photo = models.TextField(blank=True)
    content = models.JSONField()
    date_created = models.DateTimeField(default=timezone.now)
    actual_tags = models.ManyToManyField("ActualTag", blank=True)

    class Meta:
        verbose_name = "actual"
        verbose_name_plural = "actual"
        ordering = ['-date_created']

class ActualTag(BaseUUID): 
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "actual tag"
        verbose_name_plural = "actual tags"
        ordering = ['name']