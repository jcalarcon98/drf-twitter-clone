# Generated by Django 3.1.7 on 2021-04-15 03:18

import apps.utils.general
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20210413_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=apps.utils.general.upload_to),
        ),
    ]
