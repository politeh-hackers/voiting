# Generated by Django 5.1.4 on 2025-01-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appeals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appeal',
            name='category',
        ),
        migrations.AddField(
            model_name='appeal',
            name='category',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
