import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import JSONField


class MaterialCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категрии'

    def __str__(self):
        return self.name


class Material(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Код")
    category = models.ForeignKey('MaterialCategory', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=512, verbose_name="Наименовние")
    price = models.FloatField(default=0.0, verbose_name="Закупочная себестоимость")
    info = JSONField(null=True, blank=True, verbose_name="Дополнительные характеристики")

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
    material = models.ForeignKey('Material', on_delete=models.CASCADE, related_name='supply_orders',
                                 verbose_name="Материал")
    count_in = models.FloatField(default=0.0, verbose_name="Количество")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время поступления")
    responsive_user = models.ForeignKey('main.User', on_delete=models.CASCADE, verbose_name="Ответственный")

    class Meta:
        verbose_name = 'Заявка на снабжение'
        verbose_name_plural = 'Заявки на снабжение'

    def __repr__(self):
        return self.material.name

    def __str__(self):
        return self.__repr__


class UsageOrder(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE, verbose_name="Материал")
    count_out = models.FloatField(default=0.0, verbose_name="Количество")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время выдачи")

    class Meta:
        verbose_name = 'Выдача'
        verbose_name_plural = 'Выдачи'

    def __str__(self):
        return f'{self.date}_{self.material}'

    def clean(self):
        if self.material.count < self.count_out:
            raise ValidationError(f'Нельзя списать {self.count_out} из {self.material.count}')
        super().clean()
