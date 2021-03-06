from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.utils.tests.login import Login


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


class UserViewSetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.testing_user_one = get_user_model().objects.create_user(email='testing@gmail.com', password='1234',
                                                                    name='Testing')
        cls.testing_user_two = get_user_model().objects.create_user(email='testing2@gmail.com', password='1234',
                                                                    name='Testing2')

        cls.uuid = cls.testing_user_one.uuid
        cls.follower_uuid = cls.testing_user_two.uuid

    def setUp(self) -> None:
        access_token = Login.get_user_access_token(self.testing_user_one.email, '1234').get('access')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_partial_update_user(self):
        new_user_name = 'Juanito'
        patch_url = reverse('api:user-detail', kwargs={'uuid': self.uuid})
        response = self.client.patch(patch_url, {'name': new_user_name})
        updated_user = get_user_model().objects.get(uuid=self.uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.name, new_user_name)

    def test_follow_user(self):
        requested_data = {
            'action': 'FOLLOW',
            'follow_uuid': self.follower_uuid
        }
        patch_url = reverse('api:user-detail', kwargs={'uuid': self.uuid})
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        followed_user = get_user_model().objects.get(uuid=self.follower_uuid)
        self.assertEqual(followed_user.followers.count(), 1)

    def test_follow_user_that_already_follows(self):
        # First follow user
        requested_data = {
            'action': 'FOLLOW',
            'follow_uuid': self.follower_uuid
        }
        patch_url = reverse('api:user-detail', kwargs={'uuid': self.uuid})
        self.client.patch(patch_url, requested_data)
        # Execute again the follow user to the same user
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_nonexistent_user(self):
        requested_data = {
            'action': 'UNFOLLOW',
            'follow_uuid': self.follower_uuid
        }
        patch_url = reverse('api:user-detail', kwargs={'uuid': self.uuid})
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_existent_user(self):
        # First follow user
        requested_data = {
            'action': 'FOLLOW',
            'follow_uuid': self.follower_uuid
        }
        patch_url = reverse('api:user-detail', kwargs={'uuid': self.uuid})
        self.client.patch(patch_url, requested_data)
        # Unfollow user
        requested_data = {
            'action': 'UNFOLLOW',
            'follow_uuid': self.follower_uuid
        }
        patch_url = reverse('api:user-detail', kwargs={'uuid': self.uuid})
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        unfollowed_user = get_user_model().objects.get(uuid=self.follower_uuid)
        self.assertEqual(unfollowed_user.followers.count(), 0)
