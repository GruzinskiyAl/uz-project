# Generated by Django 2.2.6 on 2019-11-18 20:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_material_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
