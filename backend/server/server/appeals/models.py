from django.db import models
from base.models import BaseUUID
from category.models import Category

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
    date = models.DateField()
    text = models.CharField(max_length=500)
    photos = models.CharField(max_length=255, null=True, blank=True)
    official_response = models.CharField(max_length=500, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Appeals"
        verbose_name = "Appeal"
