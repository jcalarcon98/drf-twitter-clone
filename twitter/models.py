from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    content = models.TextField(max_length=300)


class Tweet(models.Model):
    owner = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    comments = models.ManyToManyField(User, related_name='tweet', blank=True, through=Comment)
    timestamp = models.DateTimeField(auto_now_add=True)
