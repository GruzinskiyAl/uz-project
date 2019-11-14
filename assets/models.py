import uuid
from django.db import models
from django.utils.functional import cached_property
from picklefield.fields import PickledObjectField
from datetime import date, timedelta

from main.models import User


class AssetType(models.Model):
    name = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'Тип актива'
        verbose_name_plural = 'Типы активов'

    def __str__(self):
        return self.name


class Asset(models.Model):
    asset_type = models.ForeignKey('AssetType', on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    info = PickledObjectField()

    class Meta:
        verbose_name = 'Группа актива'
        verbose_name_plural = 'Группы активов'

    def __str__(self):
        return f'{self.pk}_{self.name}'


class AssetItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    date_acquire = models.DateField(auto_now_add=True)
    sum_acquire = models.FloatField(default=0.0)
    years_to_use = models.FloatField(default=1.0)

    class Meta:
        verbose_name = 'Еденица актива'
        verbose_name_plural = 'Активы'

    def __str__(self):
        return f'{self.pk}_{self.name}'

    @cached_property
    def date_expire(self):
        days_to_use = self.years_to_use * 365
        delta = timedelta(days=days_to_use)
        return self.date_acquire + delta

    @property
    def amortization_used(self):  # hom much 'money' item already has used
        today = date.today()
        delta_days = (today - self.date_acquire).days
        if delta_days > 0:
            return self.sum_acquire / ((self.years_to_use * 365) / delta_days)
        return self.sum_acquire

    @property
    def amortization_left(self):
        return self.sum_acquire - self.amortization_used


class SupportTicket(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    respondent = models.ManyToManyField('main.User')
    time_planned = models.DateTimeField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Ремонтные работы'
        verbose_name_plural = 'Ремонтные работы'

    def __str__(self):
        return f'{self.time_planned}_{self.description[15]}..'


class SupportTicketItem(models.Model):
    support_ticket = models.ForeignKey('SupportTicket', on_delete=models.CASCADE)
    material_order = models.ForeignKey('material.UsageOrder', on_delete=models.CASCADE)


class SupportReport(models.Model):
    support_ticket = models.ForeignKey('SupportTicket', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('main.User', on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name = 'Отчет по ремонту'
        verbose_name_plural = 'Отчеты по ремонту'

    def __str__(self):
        return self.support_ticket
