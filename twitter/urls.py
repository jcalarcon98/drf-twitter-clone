from django.urls import include, path
from rest_framework.routers import DefaultRouter

from twitter import views

app_name = 'twitter'

router = DefaultRouter()
router.register('tweet', views.TweetView)

urlpatterns = [
    path('', include(router.urls))
]