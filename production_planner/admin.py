from django.contrib import admin
from .models import Product, ProductionBatch, BatchMaterial

class BatchMaterialInline(admin.TabularInline):
    model = BatchMaterial
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_co2_reduction')
    search_fields = ('title', 'description')

@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'created_by', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('product__title', 'created_by__username')
    inlines = [BatchMaterialInline]
