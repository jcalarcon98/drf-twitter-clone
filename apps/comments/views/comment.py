from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.comments.models import Comment
from apps.comments.serializers.comment import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
