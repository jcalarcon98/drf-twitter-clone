from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twitter.models import Tweet
from twitter.serializers import TweetSerializer, TweetActionSerializer


class TweetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'action' in request.data:
            action_serializer = TweetActionSerializer(data=request.data)
            if action_serializer.is_valid():
                if action_serializer.data.get('action') == 'LIKE':
                    instance.likes.add(request.user)
                else:
                    instance.likes.remove(request.user)
                instance.save()
                serializer = TweetSerializer(data=request.data, instance=instance, partial=True)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            return Response(action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tweet_serializer = TweetSerializer(data=request.data, instance=instance, context={'request': request})
        if tweet_serializer.is_valid():
            tweet_serializer.save()
            return Response(tweet_serializer.data, status=status.HTTP_201_CREATED)
        return Response(tweet_serializer.errors, status.HTTP_400_BAD_REQUEST)
