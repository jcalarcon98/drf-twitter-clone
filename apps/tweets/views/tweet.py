from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tweets.models import Tweet
from apps.tweets.serializers.tweet import TweetSerializer, ActionSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
    Simple viewset for viewing and editing accounts
    """
    permission_classes = [IsAuthenticated]
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

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
            if action == 'RETWEET':
                pass
        tweet_serializer = TweetSerializer(data=request.data, instance=current_tweet, partial=True,
                                           context={'request', request})
        if not tweet_serializer.is_valid():
            return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tweet_serializer.save()
        return Response(tweet_serializer.data, status=status.HTTP_200_OK)