from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Material(models.Model):
    """
    Represents materials required for production.
    """
    name = models.CharField(max_length=255)
    sustainable_rating = models.IntegerField(
        help_text="A rating from 1-10 indicating the sustainability of the material."
    )
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    """
    Tracks current stock levels of materials and finished products.
    """
    stock_level = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.content_object} - Stock: {self.stock_level}"
