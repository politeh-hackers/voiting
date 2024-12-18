# Generated by Django 5.1.4 on 2024-12-18 09:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('h1', models.CharField(blank=True, max_length=60)),
                ('title', models.CharField(blank=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=160)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('on_website', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('text', models.CharField(max_length=500)),
                ('photos', models.CharField(blank=True, max_length=255, null=True)),
                ('official_response', models.CharField(blank=True, max_length=500, null=True)),
                ('category', models.ManyToManyField(blank=True, to='category.category')),
            ],
            options={
                'verbose_name': 'Appeal',
                'verbose_name_plural': 'Appeals',
                'ordering': ['-date'],
            },
        ),
    ]
