from django.db import models
import uuid

class BaseUUID(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        abstract = True