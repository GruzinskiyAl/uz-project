import uuid
from django.db import models
from django.utils.functional import cached_property
from datetime import date, timedelta

from django.contrib.postgres.fields import JSONField

from main.models import User


class AssetType(models.Model):
    name = models.CharField(max_length=1024)

    class Meta:
        verbose_name = 'Тип актива'
        verbose_name_plural = 'Типы активов'

    def __str__(self):
        return self.name


class Asset(models.Model):
    asset_type = models.ForeignKey('AssetType', on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    info = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'

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
        verbose_name_plural = 'Еденицы активов'

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
            value = self.sum_acquire / ((self.years_to_use * 365) / delta_days)
        else:
            value = self.sum_acquire
        return round(value, 2)

    @property
    def amortization_left(self):
        return self.sum_acquire - self.amortization_used

    @property
    def support_count(self):
        return self.support_tickets.count()

    @property
    def last_support(self):
        support_ticket = self.support_tickets.all().order_by('time_planned').last()
        if support_ticket:
            return support_ticket.time_planned
        return ''


class SupportTicket(models.Model):
    asset_item = models.ForeignKey('AssetItem', on_delete=models.CASCADE, related_name='support_tickets')
    time_created = models.DateTimeField(auto_now_add=True)
    respondent = models.ManyToManyField('main.User')
    time_planned = models.DateTimeField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Ремонтные работы'
        verbose_name_plural = 'Ремонтные работы'

    def __str__(self):
        return f'{self.time_planned}_{self.description[:15]}..'

    @property
    def support_ticket_count(self):
        return self.support_ticket_items.count()


class SupportTicketItem(models.Model):
    support_ticket = models.ForeignKey('SupportTicket', on_delete=models.CASCADE,
                                       related_name='support_ticket_items')
    material_order = models.ForeignKey('material.UsageOrder', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ордер на материалы'
        verbose_name_plural = 'Ордеры на материалы'

    def __str__(self):
        return f'Ордер на метериал {self.pk}'


class SupportReport(models.Model):
    support_ticket = models.ForeignKey('SupportTicket', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('main.User', on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name = 'Отчет по ремонту'
        verbose_name_plural = 'Отчеты по ремонту'

    def __str__(self):
        return str(self.support_ticket)
