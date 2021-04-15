from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, serializers


class UserManagerTests(TestCase):

    def test_create_user(self):
        user_email = 'jean.alarcon@unl.edu.ec'
        user_password = '1234'
        user = get_user_model().objects.create_user(email=user_email, password=user_password)
        self.assertEqual(user.email, user_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            get_user_model().objects.create_user()
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(email='')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='testing_pass')

    def test_create_superuser(self):
        admin_user_password = 'adminPass'
        admin_user_email = 'testing.email@unl.edu.ec'
        admin_user = get_user_model().objects.create_superuser(email=admin_user_email, password=admin_user_password)
        self.assertEqual(admin_user.email, admin_user_email)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(email=admin_user_email, password=admin_user_password,
                                                      is_superuser=False)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(email=admin_user_email, password=admin_user_password,
                                                      is_staff=False)


class CreateUserViewTests(TestCase):

    def setUp(self):
        self.new_user = {
            'name': 'Testing',
            'email': 'testing@gmail.com',
            'password': 'password',
            'confirm_password': 'password',
        }
        self.url = reverse('api:user-list')

    def test_create_user(self):
        response = self.client.post(self.url, self.new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_different_passwords_on_create_user(self):
        self.new_user['confirm_password'] = 'nomatter'
        response = self.client.post(self.url, self.new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_data(self):
        del self.new_user['password']
        response = self.client.post(self.url, self.new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)