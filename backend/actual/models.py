from django.db import models
from base.models import BaseUUID
from django.utils import timezone

class Actual(BaseUUID): 
<<<<<<< HEAD
    h1 = models.CharField(max_length=60, blank=True, unique=False)
    title = models.CharField(max_length=80, blank=True, unique=False)
    description = models.CharField(max_length=160, blank=True, unique=False)
=======
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
>>>>>>> 96b43e9ec350e64ddf492b04207802a0873bb912
    header = models.CharField(max_length=200, unique=True, null=False)
    summary = models.CharField(max_length=100, blank=True, unique=True, null=False)
    main_photo = models.TextField(blank=True, null=False)
    content = models.JSONField(null=False)
    date_created = models.DateTimeField(null=False)
<<<<<<< HEAD
    actual_tags = models.CharField(max_length=100, unique=False)
=======
    actual_tags = models.CharField(max_length=100)
>>>>>>> 96b43e9ec350e64ddf492b04207802a0873bb912

    class Meta:
        verbose_name = "actual"
        verbose_name_plural = "actual"
        ordering = ['-date_created']
