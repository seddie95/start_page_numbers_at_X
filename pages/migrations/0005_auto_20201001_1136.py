# Generated by Django 3.1.1 on 2020-10-01 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20201001_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worddoc',
            name='time',
            field=models.TimeField(verbose_name=datetime.datetime(2020, 10, 1, 11, 36, 32, 339017)),
        ),
    ]