# Generated by Django 2.2.6 on 2019-11-19 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_remove_assetitem_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetitem',
            name='uuid',
        ),
    ]
