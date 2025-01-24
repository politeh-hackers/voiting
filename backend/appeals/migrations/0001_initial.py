# Generated by Django 5.1.4 on 2025-01-24 09:04

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('h1', models.CharField(blank=True, max_length=60)),
                ('title', models.CharField(blank=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=160)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('patronymic', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('on_website', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('text', models.CharField(blank=True, max_length=200)),
                ('photos', models.ImageField(blank=True, upload_to='static/images')),
                ('official_response', models.CharField(blank=True, max_length=500, null=True)),
                ('category', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Appeal',
                'verbose_name_plural': 'Appeals',
                'ordering': ['-date'],
            },
        ),
    ]
