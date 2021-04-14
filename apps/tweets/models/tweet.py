from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='retweet')
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    image = models.ImageField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, through=TweetLike, related_name='tweet')
    created_at = models.DateTimeField(auto_now_add=True)
