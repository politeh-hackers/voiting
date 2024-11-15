# Generated by Django 5.1.3 on 2024-11-15 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actual',
            fields=[
                ('media_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.media')),
            ],
            options={
                'verbose_name': 'актуальные',
                'verbose_name_plural': 'актуальные',
                'ordering': ['-date_created'],
            },
            bases=('pages.media',),
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ['-date_created'], 'verbose_name': 'медиа', 'verbose_name_plural': 'медиа'},
        ),
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
