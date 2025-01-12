from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Prefetch
from django.core.cache import cache

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        message = self.get_object()
        history = message.history.all()
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete_user(self, request):
        sender=request.user
        sender.delete()
        return Response({"message": "Your User account has been deleted successfully"}, status=status.HTTP_200_OK)
  
@cache(60)
class ThreadedConversationView(APIView):
    def get(self, request, conversation_id):
        messages = Message.objects.filter(parent_message=None, receiver_id=conversation_id).prefetch_related(
            'replies__replies',
        ).select_related('sender', 'receiver')

        data = [
            {
                "id": message.id,
                "content": message.content,
                "timestamp": message.timestamp,
                "replies": self.get_threaded_replies(message)
            }
            for message in messages
        ]
        return Response(data, status=status.HTTP_200_OK)

        
    def get_threaded_replies(self, message):
        """
        Recursively fetch all replies for a given message.
        """
        replies = []
        for reply in message.replies.all():
            replies.append({
                'message': reply,
                'replies': self.get_threaded_replies(reply)  # Recursive call
            })
        return replies
    
    
class UnreadMessagesView(APIView):
    def get(self, request):
        user = request.user
        unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp')

        data = [
            {
                "id": message.id,
                "sender": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp,
            }
            for message in unread_messages
        ]
        return Response(data, status=status.HTTP_200_OK)