from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Media(models.Model):
    h1 = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=160, blank=True)
    header = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='media_images/')
    date_created = models.DateTimeField(default=timezone.now)

    def validation(self):
        if not (10 <= len(self.h1) <= 60):
            raise ValidationError("h1 должен быть от 10 до 60 символов.")
        if not (30 <= len(self.title) <= 80):
            raise ValidationError("Title должен быть от 30 до 80 символов.")
        if not (80 <= len(self.description) <= 160):
            raise ValidationError("Description должен быть от 80 до 160 символов.")
        if not (10 <= len(self.header) <= 200):
            raise ValidationError("Header должен быть до 200 символов.")

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.header[:160]
        if not self.title:
            self.title = self.description[:80]
        if not self.h1:
            self.h1 = self.title[:60]
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Медиа статья"
        verbose_name_plural = "Медиа статьи"
        ordering = ['-date_created']
