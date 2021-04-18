from django.contrib import admin

# Register your models here.
from apps.authentication.models import User

admin.site.register(User)
