from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("can_publish", "Can publish posts"),
        ]