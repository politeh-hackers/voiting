# Generated by Django 5.1.3 on 2025-01-20 19:26

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('h1', models.CharField(blank=True, max_length=60)),
                ('title', models.CharField(blank=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=160)),
                ('header', models.CharField(blank=True, max_length=200, unique=True)),
                ('main_photo', models.TextField(blank=True)),
                ('content', models.JSONField()),
                ('date_created', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': 'biography',
                'verbose_name_plural': 'biography',
            },
        ),
    ]
