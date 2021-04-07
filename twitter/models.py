from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    owner = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.FileField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(get_user_model(), related_name='tweet', blank=True, through=TweetLike)
    timestamp = models.DateTimeField(auto_now_add=True)
