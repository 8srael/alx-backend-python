"""
    Serializers for Message, user and Conversation models 
"""

from rest_framework import serializers
from .models import user, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Include sender details

    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Include participant details
    messages = MessageSerializer(many=True, read_only=True, source='message_set')  # Include messages

    class Meta:
        model = Conversation
        fields = '__all__'
