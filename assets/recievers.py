from django.dispatch import receiver
from django.db import models
from assets.models import AssetItemSupplyOrder, AssetItem


@receiver(models.signals.post_save, sender=AssetItemSupplyOrder, dispatch_uid='execute_after_save')
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        asset = instance.asset
        data = {
            'asset': asset,
            'sum_acquire': round(instance.total_price/instance.count_in, 2)
        }
        AssetItem.objects.bulk_create([AssetItem(**data) for _ in range(instance.count_in)])
