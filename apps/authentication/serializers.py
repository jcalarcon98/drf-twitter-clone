from builtins import staticmethod

from django.contrib.auth import get_user_model
from django.templatetags.static import static
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class FollowerOrFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'name',
            'username',
            'profile_picture'
        )


class UserSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    followers = FollowerOrFollowingSerializer(many=True)
    following = FollowerOrFollowingSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = (
            'name',
            'username',
            'profile_picture',
            'uuid',
            'following',
            'following_count',
            'followers',
            'followers_count'
        )

    @staticmethod
    def get_following_count(self):
        return self.following.count()

    @staticmethod
    def get_followers_count(self):
        return self.followers.count()


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True,
                                             label='Confirm password')

    email = serializers.EmailField(validators=[
        UniqueValidator(
            queryset=get_user_model().objects.all(),
            message="This email is already in use.",
        )]
    )

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    'password': "Error: The passwords didn't match"
                }
            )

        user = self.Meta.model(name=name, email=email)
        user.set_password(password)
        user.save()
        return user
