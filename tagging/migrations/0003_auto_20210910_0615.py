# Generated by Django 3.2.5 on 2021-09-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0002_tag_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='AnimalID',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='ImageID',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='UUID',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
