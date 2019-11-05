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
    MATERIAL = 0
    FINANCIAL = 1
    IMMATERIAL = 2
    ASSET_TYPE = (
        (MATERIAL, 'material'),
        (FINANCIAL, 'financial'),
        (IMMATERIAL, 'immaterial')
    )
    asset_type = models.PositiveSmallIntegerField(choices=ASSET_TYPE)