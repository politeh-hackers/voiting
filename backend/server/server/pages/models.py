from django.db import models
from django.db.models import CharField
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Basic(models.Model):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class Media(Basic):
    header = models.CharField("заголовок", max_length=200)
    content = models.TextField("контент")
    image = models.ImageField("фото", upload_to='media_photos/')
    date_created = models.DateTimeField("дата", default=timezone.now)

    class Meta:
        verbose_name = "медиа"
        verbose_name_plural = "медиа"
        ordering = ['-date_created']

class Actual(Media):
    class Meta:
        verbose_name = "актуальные"
        verbose_name_plural = "актуальные"
        ordering = ['-date_created']

class Category(models.Model):
    name = models.CharField("название категории", max_length=100, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

class Appeal(Basic):
    STATUS_CHOICES = [
        ('PENDING', 'Принято в работу'),
        ('COMPLETED', 'Исполнено'),
        ('REJECTED', 'Отклонено'),
    ]

    last_name = models.CharField("Surname", max_length=100)
    first_name = models.CharField("Name", max_length=100)
    patronymic = models.CharField("Second Name", max_length=100)
    phone = models.CharField("Phone number", max_length=100)
    location = models.CharField("Location", max_length=255, blank=True)
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default='PENDING')
    on_website = models.BooleanField("isActive", default=False)
    date = models.DateField("Date", default=timezone.now)

    # static
    text = models.CharField(max_length=500)
    photos = models.CharField(max_length=255, null=True)
    official_response = models.CharField(max_length=500, null=True)

    # relation
    category = models.ManyToManyField(Category, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"




