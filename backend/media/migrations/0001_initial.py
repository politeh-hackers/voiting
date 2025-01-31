# Generated by Django 5.1.4 on 2025-01-31 09:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('slug', models.SlugField(unique=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('h1', models.CharField(blank=True, max_length=60)),
                ('title', models.CharField(blank=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=160)),
                ('header', models.CharField(blank=True, max_length=200, unique=True)),
                ('summary', models.CharField(blank=True, max_length=100, unique=True)),
                ('main_photo', models.TextField(blank=True)),
                ('date_created', models.DateField(blank=True)),
                ('media_tags', models.CharField(max_length=100)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'media',
                'verbose_name_plural': 'media',
                'ordering': ['-date_created'],
            },
        ),
    ]
