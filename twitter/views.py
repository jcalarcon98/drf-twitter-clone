from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twitter.models import Tweet
from twitter.serializers import TweetSerializer


class TweetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
