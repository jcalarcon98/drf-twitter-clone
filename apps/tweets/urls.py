from rest_framework.routers import SimpleRouter

from apps.tweets.views.tweet import TweetViewSet

router = SimpleRouter()
router.register('tweets', TweetViewSet)
