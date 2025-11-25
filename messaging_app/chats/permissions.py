# Permissions: Users can only access their conversations and messages.
from rest_framework.permissions import BasePermissions

class IsConversationParticipant(BasePermissions):
    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Conversation instance
        return request.user in obj.participants.all()
    
class IsMessageOwner(BasePermissions):
    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Message instance
        return request.user == obj.sender