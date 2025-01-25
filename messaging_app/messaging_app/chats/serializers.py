"""
    Serializers for Message, user and Conversation models 
"""

from rest_framework import serializers
from .models import user, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # Add a computed field for full name

    class Meta:
        model = user
        fields = ['user_id', 'first_name', 'last_name', 'full_name', 'email', 'role', 'phone_number', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"  # Custom logic to compute the full name

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Include sender as StringRelatedField
    sender_email = serializers.CharField(source='sender.email', read_only=True)  # Include sender email as CharField

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_email', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if len(value) < 10:  # Validate that the message body is at least 10 characters
            raise serializers.ValidationError("Message body must be at least 10 characters long.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested UserSerializer
    messages = MessageSerializer(many=True, read_only=True, source='message_set')  # Nested MessageSerializer

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']