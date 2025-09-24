from rest_framework import serializers
from .models import ProductionBatch, Product, BatchMaterial
from inventory.models import Material

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'sustainable_rating']

class ProductionBatchSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductionBatch
        fields = [
            'id',
            'product',
            'quantity',
            'materials',
            'created_by',
            'created_at',
            'total_material_cost'
        ]
        read_only_fields = ['created_by', 'created_at', 'total_material_cost']

    def validate_quantity(self, value):
        """
        Check that the batch quantity is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value