from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from apps.tweets.models.tweet import TweetLike


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TweetLike
        fields = '__all__'
