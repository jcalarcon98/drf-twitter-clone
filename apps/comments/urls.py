from rest_framework.routers import DefaultRouter

from apps.comments.views.comment import CommentViewSet

router = DefaultRouter()
router.register('comments', CommentViewSet)
