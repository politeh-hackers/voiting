from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class BaseMetaValidationConstants:
    MIN_H1_VALUE = 10
    MAX_H1_VALUE = 60
    MIN_TITLE_VALUE = 30
    MAX_TITLE_VALUE = 80
    MIN_DESCRIPTION_VALUE = 80
    MAX_DESCRIPTION_VALUE = 160

class BaseModelValidationConstants:
    MIN_HEADER_VALUE = 10
    MAX_HEADER_VALUE = 200


class Basic(models.Model):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)

    def validation(self):
        if not (BaseMetaValidationConstants.MIN_H1_VALUE <= BaseMetaValidationConstants.MAX_H1_VALUE):
            raise ValidationError("h1 должен быть от 10 до 60 символов.")
        if not (BaseMetaValidationConstants.MIN_TITLE_VALUE <= BaseMetaValidationConstants.MAX_TITLE_VALUE):
            raise ValidationError("Title должен быть от 30 до 80 символов.")
        if not (BaseMetaValidationConstants.MIN_DESCRIPTION_VALUE <= BaseMetaValidationConstants.MAX_DESCRIPTION_VALUE):
            raise ValidationError("Description должен быть от 80 до 160 символов.")

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.header
        if not self.title:
            self.title = self.description
        if not self.h1:
            self.h1 = self.title
        super(Basic, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Media(Basic):
    header = models.CharField("заголовок", max_length=200)
    content = models.TextField("контент")
    image = models.ImageField("фото", upload_to='media_images/')
    date_created = models.DateTimeField("дата", default=timezone.now)

    def validation(self):
        super().validation()
        if not (BaseModelValidationConstants.MIN_HEADER_VALUE <= BaseModelValidationConstants.MAX_HEADER_VALUE):
            raise ValidationError("Header должен быть от 10 до 200 символов.")
        super().save()

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

    last_name = models.CharField("фамилия", max_length=100, validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁё]+$')])
    first_name = models.CharField("имя", max_length=100, validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁё]+$')])
    patronymic = models.CharField("отчество", max_length=100, validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁё]+$')])
    phone = models.CharField("телефон", max_length=100, validators=[RegexValidator(r'^\+375\d{9}$')])
    location = models.CharField("точка на карте", max_length=255, blank=True)
    text = models.TextField("текст обращения", validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁё.,!?;:()\- ]+$')])
    photos = models.ImageField("фото", upload_to='appeal_photos/', blank=True, null=True)
    official_response = models.TextField("официальный ответ", validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁё.,!?;:()\- ]+$')], blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField("статус", max_length=10, choices=STATUS_CHOICES, default='PENDING')
    on_website = models.BooleanField("присутсвие на сайте", default=False)
    date = models.DateField("дата", default=timezone.now)

    def validation(self):
        super().validation()
        if not self.description:
            self.description = "Обращение от " + self.last_name + " " + self.first_name + " " + str(self.category)
        if not (BaseModelValidationConstants.MIN_HEADER_VALUE <= BaseModelValidationConstants.MAX_HEADER_VALUE):
            raise ValidationError("Header должен быть от 10 до 200 символов.")

    def save(self, *args, **kwargs):
        if self.pk:
            existing_appeal = Appeal.objects.get(pk=self.pk)
            if (existing_appeal.last_name != self.last_name or
                existing_appeal.first_name != self.first_name or
                existing_appeal.patronymic != self.patronymic or
                existing_appeal.phone != self.phone or
                existing_appeal.location != self.location):
                raise ValidationError("Невозможно изменить фамилию, имя, отчество, номер телефона или точку на карте.")
        if not self.description:
            self.description = f"Обращение от {self.first_name} {self.last_name} ({self.category})"
        if not self.title:
            self.title = self.description
        if not self.h1:
            self.h1 = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обращение от {self.first_name} {self.last_name} ({self.category})"

    class Meta:
        ordering = ['-date']
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"

