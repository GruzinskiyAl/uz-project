from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    PRODUCT_MANAGER = 0
    PROJECT_MANAGER = 1
    ENGINEER = 2
    USER_POSITION = (
        (PRODUCT_MANAGER, 'product_manager'),
        (PROJECT_MANAGER, 'project_manager'),
        (ENGINEER, 'engineer')
    )
    position = models.PositiveSmallIntegerField(choices=USER_POSITION, null=True, blank=True)
    phone = models.CharField(max_length=64, blank=True, null=True)


class BaseAsset(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)
    name = models.CharField(max_length=512)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class MaterialAsset(BaseAsset):
    count = models.PositiveIntegerField(default=1)

class MaterialAssetOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class FinancialAsset(BaseAsset):
    pass


class ImmaterialAsset(BaseAsset):
    pass


class MartialAssetSupport(models.Model):
    pass
