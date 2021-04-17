from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tweets.urls import router as tweet_router
from apps.comments.urls import router as comment_router
from apps.authentication.urls import router as user_router
app_name = 'api'

urlpatterns = [
    path('auth/', include('apps.authentication.urls', namespace='authentication')),
]

router = DefaultRouter()
router.registry.extend(tweet_router.registry)
router.registry.extend(comment_router.registry)
router.registry.extend(user_router.registry)

urlpatterns += router.urls
