# Generated by Django 3.1.1 on 2020-10-01 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_delete_numbereddoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worddoc',
            name='doc_file',
            field=models.FileField(upload_to='unprocessed'),
        ),
    ]
