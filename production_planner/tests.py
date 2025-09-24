from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
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

class ProductionBatchAPITest(APITestCase):
    def setUp(self):
        self.factory_manager_user = User.objects.create_user(username='factory_manager', password='password')
        self.factory_manager_user.profile.role = 'FACTORY_MANAGER'
        self.factory_manager_user.profile.save()
        self.factory_manager_token = Token.objects.create(user=self.factory_manager_user)

        self.demand_planner_user = User.objects.create_user(username='demand_planner', password='password')
        self.demand_planner_user.profile.role = 'DEMAND_PLANNER'
        self.demand_planner_user.profile.save()
        self.demand_planner_token = Token.objects.create(user=self.demand_planner_user)
        
        self.product = Product.objects.create(title='API Test Product', target_co2_reduction=2.0)

    def test_demand_planner_cannot_create_batch(self):
        """
        Ensure demand planners cannot create new production batches.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.demand_planner_token.key)
        url = '/production/api/batches/'
        data = {'product_id': self.product.id, 'quantity': 100}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_factory_manager_can_create_batch(self):
        """
        Ensure factory managers can create new production batches.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.factory_manager_token.key)
        url = '/production/api/batches/'
        data = {'product_id': self.product.id, 'quantity': 100}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_quantity_validation(self):
        """
        Test that the quantity validation in the serializer works.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.factory_manager_token.key)
        url = '/production/api/batches/'
        data = {'product_id': self.product.id, 'quantity': -10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)
