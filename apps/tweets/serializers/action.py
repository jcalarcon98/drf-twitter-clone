from rest_framework import serializers


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
