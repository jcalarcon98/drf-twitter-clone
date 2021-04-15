from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.serializers import CustomTokenObtainPairSerializer, RegisterUserSerializer, UserSerializer
from apps.utils.permissions import IsTheSameUserOrReadOnly


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTheSameUserOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny(), ]
        return super(UserViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        register_serializer = RegisterUserSerializer(data=request.data)
        if register_serializer.is_valid():
            new_user = register_serializer.save()
            if new_user:
                return Response(register_serializer.data, status=status.HTTP_201_CREATED)

        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        current_user = self.get_object()
        if 'action' in request.data:
            action = request.data['action']
            if 'follow_uuid' in request.data:
                user_to_follow = get_user_model().objects.filter(uuid=request.data['follow_uuid']).first()
                if action == 'FOLLOW':
                    current_user.following.add(user_to_follow)
                elif action == 'UNFOLLOW':
                    current_user.following.remove(user_to_follow)

        user_serializer = UserSerializer(data=request.data, instance=current_user, partial=True,
                                         context={'request': request})

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def get_parsers(self):
        """
        Put this if Error with swagger appear with parsers
        :return:
        :rtype:
        """
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()
