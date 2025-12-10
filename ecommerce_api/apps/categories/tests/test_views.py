from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.categories.models import Category

class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('categories:categories-list')
        self.category = Category.objects.create(
            name='Books',
            description='All kinds of books'
        )

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Books')

    def test_retrieve_category(self):
        detail_url = reverse('categories:categories-detail', args=[self.category.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Books')

    def test_create_category(self):
        payload = {
            'name': 'Clothing',
            'description': 'Apparel and accessories'
        }
        response = self.client.post(self.list_url, payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(response.data['description'], payload['description'])
        self.assertIn('id', response.data)
        self.assertIsNotNone(response.data['created_at'])

    def test_create_category_invalid(self):
        payload = {
            'name': '',
            'description': 'No name provided'
        }
        response = self.client.post(self.list_url, payload, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)

    def test_update_category(self):
        detail_url = reverse('categories:categories-detail', args=[self.category.id])
        payload = {
            'name': 'Updated Books',
            'description': 'Updated description'
        }

        response = self.client.put(detail_url, payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(response.data['description'], payload['description'])


    def test_update_category_invalid(self):
        detail_url = reverse('categories:categories-detail', args=[self.category.id])
        payload = {
            'name': '',
            'description': 'Invalid update'
        }

        response = self.client.put(detail_url, payload, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)


    def test_delete_category(self):
        detail_url = reverse('categories:categories-detail', args=[self.category.id])

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)