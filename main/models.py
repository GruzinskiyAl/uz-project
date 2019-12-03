from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ILL = 0
    VACATION = 1
    AT_WORK = 2
    DAY_OFF = 3
    REMOTE = 4
    USER_STATUS = (
        (ILL, 'Больничный'),
        (VACATION, 'Отпуск'),
        (AT_WORK, 'На рабочем месте'),
        (DAY_OFF, 'Выходной'),
        (REMOTE, 'Удаленно')
    )
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    user_status = models.SmallIntegerField(choices=USER_STATUS, null=True, blank=True, verbose_name='Статус')
    departament = models.ForeignKey('Departament', models.CASCADE, null=True, blank=True, verbose_name='Департамент')
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Должность")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    manager = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Руководитель")

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __repr__(self):
        return self.get_full_name()

    def __str__(self):
        return self.__repr__()

    @property
    def full_name(self):
        return self.get_full_name()


class Role(models.Model):
    name = models.CharField(max_length=512, verbose_name="Название")

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class Departament(models.Model):
    name = models.CharField(max_length=512, verbose_name="Название")

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self):
        return self.name
