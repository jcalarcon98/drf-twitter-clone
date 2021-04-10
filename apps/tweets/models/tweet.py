from django.db import models

from apps.tweets.models.tweetLike import TweetLike
from config import settings

User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    image = models.CharField(blank=True, null=True)
    likes = models.ManyToManyField(User, through=TweetLike)
    created_at = models.DateTimeField(auto_now_add=True)
