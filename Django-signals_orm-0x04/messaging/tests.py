from django.test import TestCase
from django.contrib.auth.models import User
from .models import User, Message, MessageHistory, Notification

class SignalTestCase(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass123')
        self.receiver = User.objects.create_user(username='receiver', password='pass123')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello"
        )

        notification = Notification.objects.filter(user=self.receiver, message=message)

        self.assertTrue(notification.exists())
        self.assertEqual(notification.count(), 1)
        self.assertFalse(notification.first().is_read)
        
    def test_user_deletion_cleans_up_related_data(self):
        self.user.delete()
        self.assertFalse(Message.objects.filter(sender=self.user).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.user).exists())