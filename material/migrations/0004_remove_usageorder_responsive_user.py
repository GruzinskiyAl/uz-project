# Generated by Django 2.2.6 on 2019-11-20 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0003_auto_20191118_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usageorder',
            name='responsive_user',
        ),
    ]
