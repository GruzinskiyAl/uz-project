from django.db import models


def get_cash_amount():
    income = Ticket.objects.filter(ticket_type=Ticket.INCOME).aggregate(models.Sum('amount')).get('amount__sum', 0)
    outcome = Ticket.objects.filter(ticket_type=Ticket.OUTCOME).aggregate(models.Sum('amount')).get('amount__sum', 0)
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


class Ticket(models.Model):
    INCOME = 0
    OUTCOME = 1
    TICKET_TYPES = (
        (INCOME, 'income'),
        (OUTCOME, 'outcome'),
    )
    ticket_type = models.SmallIntegerField(choices=TICKET_TYPES, default=0)
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кассовый ордер'
        verbose_name_plural = 'Кассовые ордера'

    def __str__(self):
        if self.ticket_type == self.INCOME:
            prefix = '+'
        else:
            prefix = '-'
        return f'{prefix}{round(self.amount, 2)} дата - {self.date.strftime("%d.%m.%Y %H:%M")}'
