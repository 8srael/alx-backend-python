from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False)