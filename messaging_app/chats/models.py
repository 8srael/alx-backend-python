from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

# Create your models here.

# user Model that extends AbstractUser
class user(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password =  models.CharField(max_length=128, null=False, blank=False)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest',
        null=False,
        blank=False
    )
    groups = models.ManyToManyField(
        Group,
        related_name="groups", 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="permissions",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(user, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# Message Model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email} in Conversation {self.conversation.conversation_id}"