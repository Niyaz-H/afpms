from django.contrib import admin
from .models import Material, Inventory

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'sustainable_rating', 'cost_per_unit')
    search_fields = ('name',)
    list_filter = ('sustainable_rating',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'stock_level')
    search_fields = ('content_type__model',)
