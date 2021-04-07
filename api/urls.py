from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import CustomTokenObtainPairView

app_name = 'api'

urlpatterns = [
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('', include('twitter.urls', namespace='twitter'))
]
