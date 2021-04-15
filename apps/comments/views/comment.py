from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from apps.comments.models import Comment
from apps.comments.serializers.comment import CommentSerializer, CommentSerializerCreate
from apps.utils.permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_class_create = CommentSerializerCreate
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class_create
        return self.serializer_class
