from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_403_FORBIDDEN
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        
        participant_ids = request.data.get("participants", [])

        if len(participant_ids) < 2:
            raise ValidationError("A conversation must have at least two participants.")

        # Ensure all participants exist
        participants = User.objects.filter(user_id__in=participant_ids)

        if len(participants) != len(participant_ids):
            raise ValidationError("One or more participants do not exist.")
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = ConversationSerializer(conversation)
        conversation.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "Forbidden"},
                status=HTTP_403_FORBIDDEN
            )
        return super().retrieve(request, *args, **kwargs)
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = MessageFilter
    
    ordering_fields = ["created_at"]
    search_fields = ['message_body']

    
    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation")
        
        qs = Message.objects.filter(conversation__participants=self.request.user)

        if conversation_id:
            qs = qs.filter(conversation__conversation_id=conversation_id)

        return qs.order_by("sent_at")
        
    def create(self, request, *args, **kwargs):
        conversation_id = self.request.query_params.get("conversation")
        message_body = request.data.get("message_body")
        
        if not conversation_id:
            raise ValidationError("conversation field is required.")

        # Ensure conversation exists
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation not found.")

        # Ensure the user is part of the conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "Forbidden"},
                status=HTTP_403_FORBIDDEN
            )

        # Create and save the message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )