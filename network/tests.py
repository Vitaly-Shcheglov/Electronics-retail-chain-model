from decimal import Decimal

from django.test import TestCase

from .models import NetworkObject, Product, Supplier
from .serializers import NetworkNodeSerializer, NetworkObjectSerializer, ProductSerializer, SupplierSerializer


class SupplierModelTests(TestCase):

    def test_create_supplier(self):
        """Тестирование создания поставщика."""
        supplier = Supplier.objects.create(
            name="Test Supplier",
            email="supplier@example.com",
            country="Country",
            city="City",
            street="Street",
            house_number="1A",
            debt=Decimal("100.00"),
        )
        self.assertEqual(supplier.name, "Test Supplier")
        self.assertEqual(supplier.email, "supplier@example.com")
        self.assertEqual(supplier.debt, Decimal("100.00"))


class NetworkObjectModelTests(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.network_object = NetworkObject.objects.create(
            name="Network Object A", city="Test City", supplier=self.supplier, debt=Decimal("50.00")
        )

    def test_create_network_object(self):
        """Тестирование создания сетевого объекта."""
        self.assertEqual(self.network_object.name, "Network Object A")
        self.assertEqual(self.network_object.supplier.name, "Test Supplier")
        self.assertEqual(self.network_object.city, "Test City")


class ProductModelTests(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.network_object = NetworkObject.objects.create(
            name="Network Object A", city="Test City", supplier=self.supplier
        )
        self.product = Product.objects.create(
            name="Product A",
            description="Description of Product A",
            price=Decimal("25.00"),
            debt_to_supplier=Decimal("5.00"),
            supplier=self.supplier,
        )
        self.product.network_objects.add(self.network_object)

    def test_create_product(self):
        """Тестирование создания продукта."""
        self.assertEqual(self.product.name, "Product A")
        self.assertEqual(self.product.price, Decimal("25.00"))
        self.assertIn(self.network_object, self.product.network_objects.all())


class NetworkNodeSerializerTests(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.network_node_data = {
            "name": "Network Node A",
            "email": "node@example.com",
            "country": "Country",
            "city": "City",
            "street": "Street",
            "house_number": "1A",
            "supplier": self.supplier,
            "debt_to_supplier": 100.00,
        }

        """Тестирование десериализации узла сети."""
        serializer = NetworkNodeSerializer(data=self.network_node_data)
        if serializer.is_valid():
            network_node = serializer.save()
            self.assertEqual(network_node.name, "Network Node A")
            self.assertEqual(network_node.supplier.name, "Test Supplier")


class NetworkObjectSerializerTests(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.network_object_data = {
            "name": "Network Object A",
            "city": "Test City",
            "supplier": self.supplier,
            "debt": 50.00,
        }

    def test_network_object_serialization(self):
        """Тестирование сериализации сетевого объекта."""
        serializer = NetworkObjectSerializer(data=self.network_object_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Network Object A")


class SupplierSerializerTests(TestCase):

    def setUp(self):
        self.supplier_data = {"name": "Test Supplier", "email": "supplier@example.com", "debt": 200.00}

    def test_supplier_serialization(self):
        """Тестирование сериализации поставщика."""
        serializer = SupplierSerializer(data=self.supplier_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Test Supplier")

    def test_supplier_deserialization(self):
        """Тестирование десериализации поставщика."""
        serializer = SupplierSerializer(data=self.supplier_data)
        if serializer.is_valid():
            supplier = serializer.save()
            self.assertEqual(supplier.name, "Test Supplier")
            self.assertEqual(supplier.email, "supplier@example.com")


class ProductSerializerTests(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.product_data = {
            "name": "Product A",
            "description": "Description of Product A",
            "price": 25.00,
            "debt_to_supplier": 5.00,
            "supplier": self.supplier,
        }

    def test_product_deserialization(self):
        """Тестирование десериализации продукта."""
        serializer = ProductSerializer(data=self.product_data)
        if serializer.is_valid():
            product = serializer.save()
            self.assertEqual(product.name, "Product A")
            self.assertEqual(product.supplier.name, "Test Supplier")
