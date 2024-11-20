from django.db import models
from pages.models import *


class Post(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("can_publish", "Can publish posts"),
        ]