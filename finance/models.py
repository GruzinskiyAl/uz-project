from django.db import models


def get_cash_amount():
    income = CreditTicket.objects.aggregate(models.Sum('amount')).get('amount__sum', 0)
    outcome = ChargeTicket.objects.aggregate(models.Sum('amount')).get('amount__sum', 0)
    return income - outcome


class Cash(models.Model):
    amount = models.FloatField(default=get_cash_amount, editable=False)
    date = models.DateField(auto_now_add=True, unique=True)

    class Meta:
        verbose_name = 'Средства'
        verbose_name_plural = 'Средства'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date}_{self.amount}'


class BaseTicket(models.Model):
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.date}_{self.amount}'


class CreditTicket(BaseTicket):  # ПКО
    class Meta:
        abstract = False
        verbose_name = 'Приходный кассовый чек'
        verbose_name_plural = 'Приходные кассовые чеки'


class ChargeTicket(BaseTicket):  # PKO
    class Meta:
        abstract = False
        verbose_name = 'Расходнй кассовый чек'
        verbose_name_plural = 'Расходные кассовые чеки'
