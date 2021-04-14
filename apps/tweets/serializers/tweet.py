from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from apps.comments.serializers.comment import CommentSerializer
from apps.tweets.models import Tweet
from apps.tweets.serializers.like import LikeSerializer


class TweetSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    likes = LikeSerializer(source='tweetlike_set', many=True, read_only=True)
    comments = CommentSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = '__all__'

    @staticmethod
    def get_likes_count(self):
        return self.likes.count()


class TweetSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Tweet
        fields = ('content', 'image', 'created_at')
        extra_kwargs = {
            'content': {
                'error_messages': {
                    'max_length': "Tweet content is too Long"
                }
            }
        }
