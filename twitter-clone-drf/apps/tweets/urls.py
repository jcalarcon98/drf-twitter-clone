from rest_framework.routers import DefaultRouter

from apps.tweets.views.tweet import TweetViewSet

router = DefaultRouter()
router.register('tweet', TweetViewSet)
