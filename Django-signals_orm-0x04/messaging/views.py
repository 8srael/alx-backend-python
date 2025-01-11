from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        message = self.get_object()
        history = message.history.all()
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)
