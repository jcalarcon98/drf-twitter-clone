from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from apps.comments.serializers.comment import CommentSerializer
from apps.tweets.models import Tweet
from apps.tweets.serializers.like import LikeSerializer


class TweetSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    retweeted_times = serializers.SerializerMethodField()
    likes = LikeSerializer(source='tweetlike_set', many=True, read_only=True)
    comments = CommentSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = '__all__'

    @staticmethod
    def get_likes_count(self):
        return self.likes.count()

    @staticmethod
    def get_retweeted_times(self):
        return self.retweet.count()


class TweetSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    content = serializers.CharField(required=False)

    class Meta:
        model = Tweet
        fields = ('content', 'image', 'created_at', 'user', 'parent')
        extra_kwargs = {
            'content': {
                'error_messages': {
                    'max_length': "Tweet content is too Long"
                }
            }
        }

    def validate(self, data):
        if 'content' not in data:
            if 'parent' not in data:
                raise serializers.ValidationError(
                    {
                        'message': 'Content is necessary'
                    }
                )

        return data
