from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from apps.comments.serializers.comment import CommentSerializer
from apps.tweets.models import Tweet
from apps.tweets.models.tweet import TweetLike


class ActionSerializer(serializers.Serializer):
    ACTIONS = (
        ('LIKE', 'like'),
        ('UNLIKE', 'unlike'),
        ('RETWEET', 'retweet'),
    )

    action = serializers.ChoiceField(choices=ACTIONS,
                                     error_messages={'invalid_choice': 'The request action is not valid'})
    content = serializers.CharField(max_length=300, required=False,
                                    error_messages={'max_length': "Tweet content is too Long"})


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TweetLike
        fields = '__all__'


class TweetSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    likes = LikeSerializer(source='tweetlike_set', many=True, read_only=True)
    comments = CommentSerializer(many=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Tweet
        fields = '__all__'
        extra_kwargs = {
            'content': {
                'error_messages': {
                    'max_length': "Tweet content is too Long"
                }
            }
        }

    @staticmethod
    def get_likes_count(self):
        return self.likes.count()
