from rest_framework import serializers
from .models import Message, MessageHistory, Notification


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['old_content', 'edited_at', 'edited_by']

class MessageSerializer(serializers.ModelSerializer):
    history = MessageHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'user', 'edited', 'created_at', 'updated_at', 'history']
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'content', 'timestamp', 'is_read']