from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Only create a notification if the message is new
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender}"
        )
        
@receiver(pre_save, sender=Message)
def log_edit_msg(sender, instance, **kwargs):
    """
    Log the edit of a message. Save before editing.
    """
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content: 
                
                MessageHistory.objects.create(
                    message=old_message,
                    content=old_message.content
                )

                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    """
        Delete all messages and notifications related to the user
    """
    
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()