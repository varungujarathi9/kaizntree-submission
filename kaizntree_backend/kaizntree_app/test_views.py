from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Item
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class SignupApiViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')

    def test_signup_api_view(self):
        signup_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(
            self.signup_url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Signup successful')
        self.assertEqual(response.data['user']
                         ['username'], signup_data['username'])
        self.assertEqual(response.data['user']['email'], signup_data['email'])

        user = User.objects.get(username=signup_data['username'])
        self.assertEqual(user.username, signup_data['username'])
        self.assertEqual(user.email, signup_data['email'])
        self.assertTrue(user.check_password(signup_data['password']))

    def test_signup_api_view_invalid_data(self):
        invalid_signup_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': 'testpassword'
        }
        response = self.client.post(
            self.signup_url, invalid_signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email']
                         [0], 'Enter a valid email address.')


class LoginApiViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more tests as needed for your view


class LogoutApiViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout_success(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ItemListApiViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('item-list')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_item_list(self):
        item1 = Item.objects.create(
            user_id=self.user,
            SKU='SKU1',
            name='Item 1',
            category='OL',
            tags='Tag 1',
            cost='10.00',
            in_stock=10,
            available_stock=10,
            minimum_stock=5,
            desired_stock=8,
            is_assembly=True,
            is_component=False,
            is_purchaseable=True,
            is_sellable=True,
            is_bundle=False
        )
        item2 = Item.objects.create(
            user_id=self.user,
            SKU='SKU2',
            name='Item 2',
            category='OL',
            tags='Tag 2',
            cost='20.00',
            in_stock=5,
            available_stock=5,
            minimum_stock=2,
            desired_stock=4,
            is_assembly=False,
            is_component=True,
            is_purchaseable=True,
            is_sellable=True,
            is_bundle=False
        )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)
        self.assertEqual(response.data.get('results')[0]['SKU'], item1.SKU)
        self.assertEqual(response.data.get('results')[0]['name'], item1.name)
        self.assertEqual(response.data.get('results')[
                         0]['category'], item1.category)
        self.assertEqual(response.data.get('results')[0]['tags'], item1.tags)
        self.assertEqual(response.data.get('results')[0]['cost'], item1.cost)
        self.assertEqual(response.data.get('results')[
                         0]['in_stock'], item1.in_stock)
        self.assertEqual(
            response.data.get('results')[0]['available_stock'], item1.available_stock)
        self.assertEqual(
            response.data.get('results')[0]['minimum_stock'], item1.minimum_stock)
        self.assertEqual(
            response.data.get('results')[0]['desired_stock'], item1.desired_stock)
        self.assertEqual(response.data.get('results')[
                         0]['is_assembly'], item1.is_assembly)
        self.assertEqual(response.data.get('results')[
                         0]['is_component'], item1.is_component)
        self.assertEqual(
            response.data.get('results')[0]['is_purchaseable'], item1.is_purchaseable)
        self.assertEqual(response.data.get('results')[
                         0]['is_sellable'], item1.is_sellable)
        self.assertEqual(response.data.get('results')[
                         0]['is_bundle'], item1.is_bundle)
        self.assertEqual(response.data.get('results')[1]['SKU'], item2.SKU)
        self.assertEqual(response.data.get('results')[1]['name'], item2.name)
        self.assertEqual(response.data.get('results')[
                         1]['category'], item2.category)
        self.assertEqual(response.data.get('results')[1]['tags'], item2.tags)
        self.assertEqual(response.data.get('results')[1]['cost'], item2.cost)
        self.assertEqual(response.data.get('results')[
                         1]['in_stock'], item2.in_stock)
        self.assertEqual(
            response.data.get('results')[1]['available_stock'], item2.available_stock)
        self.assertEqual(
            response.data.get('results')[1]['minimum_stock'], item2.minimum_stock)
        self.assertEqual(
            response.data.get('results')[1]['desired_stock'], item2.desired_stock)
        self.assertEqual(response.data.get('results')[
                         1]['is_assembly'], item2.is_assembly)
        self.assertEqual(response.data.get('results')[
                         1]['is_component'], item2.is_component)
        self.assertEqual(
            response.data.get('results')[1]['is_purchaseable'], item2.is_purchaseable)
        self.assertEqual(response.data.get('results')[
                         1]['is_sellable'], item2.is_sellable)
        self.assertEqual(response.data.get('results')[
                         1]['is_bundle'], item2.is_bundle)

    def test_get_item_list_with_filters(self):
        item1 = Item.objects.create(
            user_id=self.user,
            SKU='SKU1',
            name='Item 1',
            category='OL',
            tags='Tag 1',
            cost='10.00',
            in_stock=10,
            available_stock=10,
            minimum_stock=5,
            desired_stock=8,
            is_assembly=True,
            is_component=False,
            is_purchaseable=True,
            is_sellable=True,
            is_bundle=False
        )

        filters = {
            'SKU': 'SKU1',
            'name': 'Item 1',
            'category': 'OL',
            'tags': 'Tag 1',
            'is_assembly': True,
            'is_component': False,
            'is_purchaseable': True,
            'is_sellable': True,
            'is_bundle': False
        }

        response = self.client.get(self.list_url, filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0]['SKU'], item1.SKU)
        self.assertEqual(response.data.get('results')[0]['name'], item1.name)
        self.assertEqual(response.data.get('results')[
                         0]['category'], item1.category)
        self.assertEqual(response.data.get('results')[0]['tags'], item1.tags)
        self.assertEqual(response.data.get('results')[0]['cost'], item1.cost)
        self.assertEqual(response.data.get('results')[
                         0]['in_stock'], item1.in_stock)
        self.assertEqual(
            response.data.get('results')[0]['available_stock'], item1.available_stock)
        self.assertEqual(
            response.data.get('results')[0]['minimum_stock'], item1.minimum_stock)
        self.assertEqual(
            response.data.get('results')[0]['desired_stock'], item1.desired_stock)
        self.assertEqual(response.data.get('results')[
                         0]['is_assembly'], item1.is_assembly)
        self.assertEqual(response.data.get('results')[
                         0]['is_component'], item1.is_component)
        self.assertEqual(
            response.data.get('results')[0]['is_purchaseable'], item1.is_purchaseable)
        self.assertEqual(response.data.get('results')[
                         0]['is_sellable'], item1.is_sellable)
        self.assertEqual(response.data.get('results')[
                         0]['is_bundle'], item1.is_bundle)

    def test_create_item(self):
        data = {
            'SKU': 'SKU4',
            'name': 'Item 4',
            'category': 'Category 4',
            'tags': 'OL',
            'cost': '10.00',
            'in_stock': 10,
            'available_stock': 10,
            'minimum_stock': 5,
            'desired_stock': 8,
            'is_assembly': True,
            'is_component': False,
            'is_purchaseable': True,
            'is_sellable': True,
            'is_bundle': False
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['SKU'], data['SKU'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['category'], data['category'])
        self.assertEqual(response.data['tags'], data['tags'])
        self.assertEqual(response.data['cost'], data['cost'])
        self.assertEqual(response.data['in_stock'], data['in_stock'])
        self.assertEqual(
            response.data['available_stock'], data['available_stock'])
        self.assertEqual(response.data['minimum_stock'], data['minimum_stock'])
        self.assertEqual(response.data['desired_stock'], data['desired_stock'])
        self.assertEqual(response.data['is_assembly'], data['is_assembly'])
        self.assertEqual(response.data['is_component'], data['is_component'])
        self.assertEqual(
            response.data['is_purchaseable'], data['is_purchaseable'])
        self.assertEqual(response.data['is_sellable'], data['is_sellable'])
        self.assertEqual(response.data['is_bundle'], data['is_bundle'])

    def test_create_item_invalid_data(self):
        data = {
            'SKU': 'SKU1',
            'name': 'Item 1',
            'category': 'Category 1',
            'tags': 'Tag 1',
            'cost': 'invalid_cost',  # Invalid cost value
            'in_stock': 10,
            'available_stock': 10,
            'minimum_stock': 5,
            'desired_stock': 8,
            'is_assembly': True,
            'is_component': False,
            'is_purchaseable': True,
            'is_sellable': True,
            'is_bundle': False
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cost', response.data)

    def test_update_item(self):
        item = Item.objects.create(
            user_id=self.user,
            SKU='SKU1',
            name='Item 1',
            category='Category 1',
            tags='OL',
            cost=10.0,
            in_stock=10,
            available_stock=10,
            minimum_stock=5,
            desired_stock=8,
            is_assembly=True,
            is_component=False,
            is_purchaseable=True,
            is_sellable=True,
            is_bundle=False
        )

        data = {
            'id': item.id,
            'name': 'Updated Item 1',
            'category': 'Updated Category 1',
            'tags': 'SQ',
            'cost': '15.00',
            'in_stock': 5,
            'available_stock': 5,
            'minimum_stock': 2,
            'desired_stock': 4,
            'is_assembly': False,
            'is_component': True,
            'is_purchaseable': True,
            'is_sellable': True,
            'is_bundle': False
        }

        response = self.client.put(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], item.id)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['category'], data['category'])
        self.assertEqual(response.data['tags'], data['tags'])
        self.assertEqual(response.data['cost'], data['cost'])
        self.assertEqual(response.data['in_stock'], data['in_stock'])
        self.assertEqual(
            response.data['available_stock'], data['available_stock'])
        self.assertEqual(response.data['minimum_stock'], data['minimum_stock'])
        self.assertEqual(response.data['desired_stock'], data['desired_stock'])
        self.assertEqual(response.data['is_assembly'], data['is_assembly'])
        self.assertEqual(response.data['is_component'], data['is_component'])
        self.assertEqual(
            response.data['is_purchaseable'], data['is_purchaseable'])
        self.assertEqual(response.data['is_sellable'], data['is_sellable'])
        self.assertEqual(response.data['is_bundle'], data['is_bundle'])

    def test_delete_item(self):
        item = Item.objects.create(
            user_id=self.user,
            SKU='SKU1',
            name='Item 1',
            category='Category 1',
            tags='Tag 1',
            cost='10.00',
            in_stock=10,
            available_stock=10,
            minimum_stock=5,
            desired_stock=8,
            is_assembly=True,
            is_component=False,
            is_purchaseable=True,
            is_sellable=True,
            is_bundle=False
        )

        data = {
            'id': item.id
        }

        response = self.client.delete(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=item.id).exists())
