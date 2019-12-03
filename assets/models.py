import uuid
from django.db import models
from django.utils.functional import cached_property
from datetime import date, timedelta

from django.contrib.postgres.fields import JSONField

from main.models import User


class AssetType(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Название")

    class Meta:
        verbose_name = 'Тип актива'
        verbose_name_plural = 'Типы активов'

    def __str__(self):
        return self.name


class Asset(models.Model):
    asset_type = models.ForeignKey('AssetType', on_delete=models.CASCADE, verbose_name="Тип актива")
    name = models.CharField(max_length=512, verbose_name="Наименование")
    years_to_use = models.FloatField(default=1.0, verbose_name="Время эксплуатации (лет)")
    info = JSONField(null=True, blank=True, verbose_name="Дополнительная информация")

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'

    def __str__(self):
        return f'{self.pk}_{self.name}'

    @property
    def supply_orders_count(self):
        return self.asset_supply_orders.count()


class AssetItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Код")
    date_acquire = models.DateField(auto_now_add=True, verbose_name="Дата поступления")
    sum_acquire = models.FloatField(default=0.0, verbose_name="Закупочная себестоимость")
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, verbose_name="Актив", related_name='asset_items')

    class Meta:
        verbose_name = 'Еденица актива'
        verbose_name_plural = 'Еденицы активов'

    def __str__(self):
        return f'{str(self.uuid)[:6]}_{self.asset.name}'

    @cached_property
    def date_expire(self):
        days_to_use = self.asset.years_to_use * 365
        delta = timedelta(days=days_to_use)
        return self.date_acquire + delta

    @cached_property
    def years_to_use(self):
        return self.asset.years_to_use

    @property
    def amortization_used(self):  # hom much 'money' item already has used
        today = date.today()
        delta_days = (today - self.date_acquire).days
        if delta_days > 0:
            value = self.sum_acquire / ((self.asset.years_to_use * 365) / delta_days)
        else:
            value = 0
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
            return support_ticket.time_planned.strftime("%d.%m.%y")
        return ''


class AssetItemSupplyOrder(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='asset_supply_orders',
                              verbose_name="Актив")
    count_in = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total_price = models.FloatField(default=0.0, verbose_name='Общая стоимость')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время заказа")

    class Meta:
        verbose_name = 'Заказ активов'
        verbose_name_plural = 'Заказы активов'

    def __str__(self):
        return f'Дата: {self.date}, актив: {self.asset}'


class SupportTicket(models.Model):
    asset_item = models.ForeignKey('AssetItem', on_delete=models.CASCADE, related_name='support_tickets',
                                   verbose_name='Еденица актива')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    respondent = models.ForeignKey('main.Departament', verbose_name="Ответственный департамент",
                                   on_delete=models.CASCADE)
    time_planned = models.DateTimeField(verbose_name="Запланированное время")
    description = models.TextField(verbose_name="Описание")

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
                                       related_name='support_ticket_items', verbose_name="Ремонтные работы")
    material_order = models.ForeignKey('material.UsageOrder', on_delete=models.CASCADE,
                                       verbose_name="Ордер на материалы")

    class Meta:
        verbose_name = 'Ордер на материалы'
        verbose_name_plural = 'Ордеры на материалы'

    def __str__(self):
        return f'Ордер на метериал {self.pk}'


class SupportReport(models.Model):
    support_ticket = models.ForeignKey('SupportTicket', on_delete=models.CASCADE, verbose_name="Ремонтные работы")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    creator = models.ForeignKey('main.User', on_delete=models.CASCADE, verbose_name="Ответственный")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = 'Отчет по ремонту'
        verbose_name_plural = 'Отчеты по ремонту'

    def __str__(self):
        return str(self.support_ticket)
