from rest_framework import serializers
from twitter.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'owner', 'likes', 'timestamp', 'comments']


class TweetActionSerializer(serializers.Serializer):
    TWEET_ACTION_OPTIONS = (
        ("LIKE", "like"),
        ("UNLIKE", "unlike"),
    )
    action = serializers.ChoiceField(choices=TWEET_ACTION_OPTIONS,
                                     error_messages={"invalid_choice": "'%s' Requested action is not permitted"})
