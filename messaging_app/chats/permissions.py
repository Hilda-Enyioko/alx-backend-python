# Permissions: Users can only access their conversations and messages.
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Conversation instance
        return request.user in obj.participants.all()
    
class IsMessageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Message instance
        return request.user == obj.sender
    

"""
Main permission class: IsParticipantOfConversation
- Ensures user is authenticated
- Ensures user is a participant in the conversation
- Ensures only participants can send, view, update, or delete messages
"""

class IsParticipantOfConversation(BasePermission):
    
    # Ensure the user is authenticated
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        
        """
        obj can be:
        - a Conversation instance (with .participants)
        - a Message instance (with .conversation.participants)
        """
        
        # Case 1: obj is a Conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # Case 2: obj is a Message
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in participants
        
        return False