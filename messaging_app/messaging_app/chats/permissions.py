# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
        Only participants of a conversation can access it.
    """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur actuel est un participant de la conversation
        return request.user in obj.participants.all()
