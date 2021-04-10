from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.serializers import CustomTokenObtainPairSerializer, RegisterUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        register_serializer = RegisterUserSerializer(data=request.data)
        if register_serializer.is_valid():
            new_user = register_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)

        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

