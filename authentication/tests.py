from django.contrib.auth import get_user_model
from django.test import TestCase


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
