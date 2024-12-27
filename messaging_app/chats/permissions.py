# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Permet l'accès aux conversations seulement pour les participants.
    """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur actuel est un participant de la conversation
        return request.user in obj.participants.all()
