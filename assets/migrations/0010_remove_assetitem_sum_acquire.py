# Generated by Django 2.2.6 on 2019-11-19 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_auto_20191119_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetitem',
            name='sum_acquire',
        ),
    ]
