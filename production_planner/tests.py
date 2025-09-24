from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Product, ProductionBatch, BatchMaterial
from inventory.models import Material, Inventory

class ProductionBatchModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(title='Test Product', target_co2_reduction=1.5)
        self.material1 = Material.objects.create(name='Cotton', sustainable_rating=8, cost_per_unit=10.00)
        self.material2 = Material.objects.create(name='Polyester', sustainable_rating=3, cost_per_unit=5.00)

        # Create initial inventory
        Inventory.objects.create(content_object=self.material1, stock_level=100)
        Inventory.objects.create(content_object=self.material2, stock_level=200)
        Inventory.objects.create(content_object=self.product, stock_level=50)

    def test_inventory_updated_on_batch_creation(self):
        """
        Test that the post_save signal correctly updates inventory when a batch is created.
        """
        batch = ProductionBatch.objects.create(
            product=self.product,
            created_by=self.user,
            quantity=10
        )
        BatchMaterial.objects.create(batch=batch, material=self.material1, quantity=20)
        BatchMaterial.objects.create(batch=batch, material=self.material2, quantity=30)

        # Check material inventory
        material_content_type = ContentType.objects.get_for_model(Material)
        self.assertEqual(Inventory.objects.get(content_type=material_content_type, object_id=self.material1.id).stock_level, 80)
        self.assertEqual(Inventory.objects.get(content_type=material_content_type, object_id=self.material2.id).stock_level, 170)

        # Check product inventory
        product_content_type = ContentType.objects.get_for_model(Product)
        self.assertEqual(Inventory.objects.get(content_type=product_content_type, object_id=self.product.id).stock_level, 60)
