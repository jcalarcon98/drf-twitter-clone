from django.conf import settings
from django.db import models

from apps.tweets.models import Tweet

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.content

