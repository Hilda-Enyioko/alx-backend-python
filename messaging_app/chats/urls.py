from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from django.contrib import admin
from django.urls import path, include

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    router.urls,
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
]
