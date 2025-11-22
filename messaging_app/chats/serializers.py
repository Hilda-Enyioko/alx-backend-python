from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message, User

class UserSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)    

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['user_id', 'created_at', 'updated_at']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['message_id', 'sent_at', 'sender_id']
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_messages(self, obj):
        msgs = obj.messages.all().order_by('sent_at')
        return MessageSerializer(msgs, many=True).data

    def validate(self, data):
        participants = self.initial_data.get('participants', [])
        if len(participants) < 2:
            raise ValidationError("A conversation must include at least two participants.")
        return data