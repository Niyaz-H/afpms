from django.db import models
from django.contrib.auth.models import User
from inventory.models import Material

class Product(models.Model):
    """
    Represents a garment design.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_co2_reduction = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Target CO2 reduction value for this product."
    )

    def __str__(self):
        return self.title


class ProductionBatch(models.Model):
    """
    Represents a planned manufacturing run.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, through='BatchMaterial')
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Batch {self.id} - {self.product.title}"

class BatchMaterial(models.Model):
    """
    Intermediary model to store the quantity of each material for a batch.
    """
    batch = models.ForeignKey(ProductionBatch, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('batch', 'material')
