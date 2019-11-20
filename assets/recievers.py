from django.dispatch import receiver
from django.db import models
from assets.models import AssetItem


@receiver(models.signals.post_save, sender=AssetItem, dispatch_uid='execute_after_save')
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        supply_order = instance.supply_order
        data = [AssetItem(**instance.data) for _ in range(supply_order.count_in)]
        AssetItem.objects.bulk_create(data)
