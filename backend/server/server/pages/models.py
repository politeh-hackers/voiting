from django.db import models
from django.utils import timezone
import uuid

class BaseUUID(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        abstract = True

class MediaTag(BaseUUID):  # Наследует только от BaseUUID
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "media tag"
        verbose_name_plural = "media tags"
        ordering = ['name']

class ActualTag(BaseUUID):  # Наследует только от BaseUUID
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "actual tag"
        verbose_name_plural = "actual tags"
        ordering = ['name']

class Category(BaseUUID):  # Наследует только от BaseUUID
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

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

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "media"
        ordering = ['-date_created']

    def __str__(self):
        return self.header

class Actual(BaseUUID): 
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
    header = models.CharField(max_length=200)
    summary = models.CharField(max_length=100, blank=True)
    main_photo = models.TextField(blank=True)
    content = models.JSONField()
    date_created = models.DateTimeField(default=timezone.now)
    actual_tags = models.ManyToManyField(ActualTag, related_name="actual", blank=True)

    class Meta:
        verbose_name = "actual"
        verbose_name_plural = "actual"
        ordering = ['-date_created']

class Appeal(BaseUUID):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    on_website = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    text = models.CharField(max_length=500)
    photos = models.CharField(max_length=255, null=True, blank=True)
    official_response = models.CharField(max_length=500, null=True, blank=True)
    category = models.ManyToManyField("Category", blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Appeals"
        verbose_name = "Appeal"