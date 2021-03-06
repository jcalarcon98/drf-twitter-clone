from django.conf import settings
from django.db import models

from apps.tweets.models import Tweet
from apps.utils.general import upload_to

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True, upload_to=upload_to)
    likes = models.ManyToManyField(User, related_name='comment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
