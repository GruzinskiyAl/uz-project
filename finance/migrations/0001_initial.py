# Generated by Django 2.2.6 on 2019-11-12 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True, unique_for_date=True)),
            ],
            options={
                'verbose_name': 'Средства',
                'verbose_name_plural': 'Средства',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='CreditTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Приходный кассовый чек',
                'verbose_name_plural': 'Приходные кассовые чеки',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChargeTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Расходнй кассовый чек',
                'verbose_name_plural': 'Расходные кассовые чеки',
                'abstract': False,
            },
        ),
    ]
