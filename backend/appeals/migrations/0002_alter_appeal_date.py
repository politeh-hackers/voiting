# Generated by Django 5.1.4 on 2024-12-19 07:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appeals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
