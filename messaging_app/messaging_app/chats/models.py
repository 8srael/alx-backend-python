from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid

# Create your models here.

class UserManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, first_name, last_name, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        
        if not email:
            raise ValueError("You must provide an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    

# user Model that extends AbstracBaseUser
class user(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password =  models.CharField(max_length=128, null=False, blank=False)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    @property
    def id(self):
        return self.user_id  # Aliasing user_id to id for compatibility

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