from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tweets.urls import router as tweets_router

app_name = 'api'

urlpatterns = [
    path('auth/', include('apps.authentication.urls', namespace='authentication')),
]

router = DefaultRouter()
router.registry.extend(tweets_router.registry)

urlpatterns += router.urls
