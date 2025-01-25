from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['participants']  # Filtrer par participants
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        # Only show conversations the user part of
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation', 'sender']
    ordering_fields = ['sent_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filterset_class = MessageFilter
    
    def get_queryset(self):
        # Only show messages in conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new message in an existing conversation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def by_conversation(self, request, pk=None):
        """
        Retrieve messages for a specific conversation.
        """
        conversation = Conversation.objects.filter(id=pk).first()
        if not conversation:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(conversation=conversation)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
