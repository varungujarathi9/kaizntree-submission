from django.test import TestCase
from django.contrib.auth.models import User
from kaizntree_app.serializers import UserSerializer, LoginSerializer, SignupSerializer, ItemSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        self.serializer = UserSerializer(data=self.user_data)

    def test_valid_serializer_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_data_contains_expected_fields(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        self.assertEqual(set(serialized_data.keys()),
                         {'username', 'email'})

    def test_serialized_data_matches_input_data(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data, self.user_data)


class LoginSerializerTestCase(TestCase):
    def setUp(self):
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.serializer = LoginSerializer(data=self.login_data)

    def test_valid_serializer_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_data_contains_expected_fields(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        self.assertEqual(set(serialized_data.keys()),
                         {'username', 'password'})

    def test_serialized_data_matches_input_data(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data, self.login_data)


class SignupSerializerTestCase(TestCase):
    def setUp(self):
        self.signup_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        self.serializer = SignupSerializer(data=self.signup_data)

    def test_valid_serializer_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_data_contains_expected_fields(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        self.assertEqual(set(serialized_data.keys()),
                         {'username', 'email'})

    def test_serialized_data_matches_input_data(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        signup_data_without_password = {
            key: value for key, value in self.signup_data.items() if key != 'password'}
        self.assertEqual(serialized_data, signup_data_without_password)

    def test_create_user(self):
        self.serializer.is_valid()
        user = self.serializer.create(self.serializer.validated_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.signup_data['username'])
        self.assertEqual(user.email, self.signup_data['email'])
        self.assertTrue(user.check_password(self.signup_data['password']))


class ItemSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a User object
        User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.item_data = {
            'user_id': 1,
            'SKU': 'ABC123',
            'name': 'Test Item',
            'category': 'Test Category',
            'tags': 'OL',
            'cost': '10.99',
            'in_stock': 1000,
            'available_stock': 500,
            'minimum_stock': 100,
            'desired_stock': 500,
            'is_assembly': False,
            'is_component': True,
            'is_purchaseable': True,
            'is_sellable': True,
            'is_bundle': False
        }
        self.serializer = ItemSerializer(data=self.item_data)

    def test_valid_serializer_data(self):
        is_valid = self.serializer.is_valid()
        if not is_valid:
            print(self.serializer.errors)
        self.assertTrue(is_valid)

    def test_serialized_data_contains_expected_fields(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data
        self.assertEqual(set(serialized_data.keys()), set(['SKU', 'name', 'category', 'tags', 'cost', 'in_stock', 'available_stock',
                         'minimum_stock', 'desired_stock', 'is_assembly', 'is_component', 'is_purchaseable', 'is_sellable', 'is_bundle']))

    def test_serialized_data_matches_input_data(self):
        self.serializer.is_valid()
        serialized_data = self.serializer.data

        item_data_without_write_only = {
            key: value for key, value in self.item_data.items() if key != 'user_id'}

        self.assertEqual(serialized_data, item_data_without_write_only)

    def test_read_only_fields(self):
        self.serializer.is_valid()
        self.assertEqual(self.serializer.Meta.read_only_fields,
                         ('id', 'updated', 'created'))

    def test_extra_kwargs(self):
        self.serializer.is_valid()
        self.assertEqual(self.serializer.Meta.extra_kwargs,
                         {'user_id': {'write_only': True}})
