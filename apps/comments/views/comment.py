from rest_framework import viewsets

from apps.comments.models import Comment
from apps.comments.serializers.comment import CommentSerializer, CommentSerializerCreate
from apps.utils.permissions import IsAuthorOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_class_create = CommentSerializerCreate

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class_create
        return self.serializer_class
