from rest_framework import serializers

from apps.tweets.models import Tweet


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


class TweetSerializer(serializers.ModelSerializer):
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