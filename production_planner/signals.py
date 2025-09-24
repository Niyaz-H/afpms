from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductionBatch
from inventory.models import Inventory

@receiver(post_save, sender=ProductionBatch)
def update_inventory_on_batch_creation(sender, instance, created, **kwargs):
    """
    Updates the inventory when a new production batch is created.
    """
    if created:
        # Decrease the stock of materials used in the batch
        for batch_material in instance.batchmaterial_set.all():
            material = batch_material.material
            quantity_to_deduct = batch_material.quantity
            
            inventory_item, created = Inventory.objects.get_or_create(
                content_type__model='material',
                object_id=material.id
            )
            inventory_item.stock_level -= quantity_to_deduct
            inventory_item.save()

        # Increase the stock of the finished product
        product = instance.product
        inventory_item, created = Inventory.objects.get_or_create(
            content_type__model='product',
            object_id=product.id
        )
        inventory_item.stock_level += instance.quantity
        inventory_item.save()