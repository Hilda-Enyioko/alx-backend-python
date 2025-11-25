from django.contrib import admin
from django.urls import path, include
from messaging_app.chats.auth import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('messaging_app.chats.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]