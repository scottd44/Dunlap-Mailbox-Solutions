# Generated by Django 3.2.5 on 2021-09-10 06:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
