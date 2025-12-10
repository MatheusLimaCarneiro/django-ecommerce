from django.test import TestCase
from apps.categories.models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Devices and gadgets'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Devices and gadgets')
        self.assertIsNotNone(self.category.created_at)

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Electronics')