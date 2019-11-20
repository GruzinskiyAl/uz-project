import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import JSONField


class MaterialCategory(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категрии'

    def __str__(self):
        return self.name


class Material(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    category = models.ForeignKey('MaterialCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    price = models.FloatField(default=0.0)
    info = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return f'{self.pk}_{self.name}'

    @property
    def count(self):
        return (SupplyOrder.objects.aggregate(models.Sum('count_in')).get('count_in__sum') or 0) - \
               (UsageOrder.objects.aggregate(models.Sum('count_out')).get('count_out__sum') or 0)

    @property
    def sum_price(self):
        return round((self.count * self.price), 2)

    @property
    def last_supply_date(self):
        if self.supply_orders.last():
            return self.supply_orders.last().date.strftime("%d.%m.%y")
        return ""


class SupplyOrder(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE, related_name='supply_orders')
    count_in = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    responsive_user = models.ForeignKey('main.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Закупка'
        verbose_name_plural = 'Закупки'

    def __str__(self):
        return self.material


class UsageOrder(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    count_out = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Выдача'
        verbose_name_plural = 'Выдачи'

    def __str__(self):
        return f'{self.date}_{self.material}'

    def clean(self):
        if self.material.count < self.count_out:
            raise ValidationError
        super().clean()
