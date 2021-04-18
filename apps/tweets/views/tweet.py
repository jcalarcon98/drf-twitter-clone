from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.tweets.models import Tweet
from apps.tweets.serializers.action import ActionSerializer
from apps.tweets.serializers.tweet import TweetSerializer, TweetSerializerCreate
from apps.utils.permissions import IsAuthorOrReadOnly


class TweetViewSet(viewsets.ModelViewSet):
    """
    Simple viewset for viewing and editing accounts
    """
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    serializer_class_create = TweetSerializerCreate
    parser_classes = [MultiPartParser, FormParser]

    def partial_update(self, request, *args, **kwargs):
        current_tweet = self.get_object()
        if 'action' in request.data:
            action_serializer = ActionSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get('action')
            if action == 'LIKE':
                current_tweet.likes.add(request.user)
            if action == 'UNLIKE':
                current_tweet.likes.remove(request.user)

        tweet_serializer = TweetSerializer(data=request.data, instance=current_tweet, partial=True,
                                           context={'request', request})
        if not tweet_serializer.is_valid():
            return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tweet_serializer.save()
        return Response(tweet_serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class_create
        return self.serializer_class

    def get_queryset(self):

        if self.action == 'list':
            user_id = self.request.query_params.get('user_id', None)
            if user_id:
                return Tweet.objects.filter(user__uuid=user_id)
        return Tweet.objects.all()

    def get_parsers(self):
        """
        Put this if Error with swagger appear with parsers
        :return:
        :rtype:
        """
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()
