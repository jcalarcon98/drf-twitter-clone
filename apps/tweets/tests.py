from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from apps.tweets.models import Tweet
from apps.utils.tests.login import Login


class TweetViewSetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(email='jean.alarcon@unl.edu.ec', password='1234',
                                                         name='Jean Carlos')
        Tweet.objects.create(content='No matter content', user=test_user)

    def setUp(self) -> None:
        access_token = Login.get_user_access_token('jean.alarcon@unl.edu.ec', '1234').get('access')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_normal_partial_update(self):
        patch_url = reverse('api:tweet-detail', args=[1])
        requested_data = {
            'content': 'new content'
        }
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tweet = Tweet.objects.get(pk=1)
        self.assertEqual(updated_tweet.content, 'new content')

    def test_like_on_partial_update(self):
        patch_url = reverse('api:tweet-detail', args=[1])
        requested_data = {
            'action': 'LIKE'
        }
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_on_partial_update(self):
        patch_url = reverse('api:tweet-detail', args=[1])
        requested_data = {
            'action': 'UNLIKE'
        }
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_action_serializer(self):
        patch_url = reverse('api:tweet-detail', args=[1])
        requested_data = {
            'action': 'INVALID_ACTION'
        }
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
