from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="testpassword")
        self.receiver = User.objects.create_user(username="receiver", password="testpassword")

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.content, "You have a new message from sender")

