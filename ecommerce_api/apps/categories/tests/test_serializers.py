from django.test import TestCase
from apps.categories.serializer import CategorySerializer

class CategorySerializerTest(TestCase):

    def test_valid_serializer(self):
        data = {
            'name': 'Games',
            'description': 'Video games'
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        data = {'name': ''}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
