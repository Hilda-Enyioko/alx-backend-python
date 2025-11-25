# Permissions: Users can only access their conversations and messages.
from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Conversation instance
        return request.user in obj.participants.all()
    
class IsMessageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Message instance
        return request.user == obj.sender