from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import ProductionBatch, Product, BatchMaterial
from inventory.models import Inventory, Material

@receiver(post_save, sender=ProductionBatch)
def update_product_inventory_on_batch_creation(sender, instance, created, **kwargs):
    """
    Increases the inventory of the finished product when a new production batch is created.
    """
    if created:
        product_content_type = ContentType.objects.get_for_model(Product)
        product = instance.product
        inventory_item, created = Inventory.objects.get_or_create(
            content_type=product_content_type,
            object_id=product.id,
            defaults={'stock_level': 0}
        )
        inventory_item.stock_level += instance.quantity
        inventory_item.save()

@receiver(post_save, sender=BatchMaterial)
def update_material_inventory_on_batch_material_creation(sender, instance, created, **kwargs):
    """
    Decreases the inventory of a material when it is added to a batch.
    """
    if created:
        material = instance.material
        quantity_to_deduct = instance.quantity
        
        material_content_type = ContentType.objects.get_for_model(Material)
        inventory_item, created = Inventory.objects.get_or_create(
            content_type=material_content_type,
            object_id=material.id,
            defaults={'stock_level': 0}
        )
        inventory_item.stock_level -= quantity_to_deduct
        inventory_item.save()