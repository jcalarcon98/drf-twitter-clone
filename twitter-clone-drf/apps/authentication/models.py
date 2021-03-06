import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=30)
    description = models.TextField(max_length=400, null=True, blank=True, default='')
    location = models.CharField(max_length=200, null=True, blank=True, default='')
    birthday = models.DateField(null=True, blank=True)
    profile_picture = models.FileField(blank=True, null=True, upload_to='user/profile/')
    cover_picture = models.FileField(blank=True, null=True, upload_to='user/cover/')
    email = models.EmailField('Email Addres', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    following = models.ManyToManyField('self', related_name='followers', blank=True, symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name + '-' + self.email
