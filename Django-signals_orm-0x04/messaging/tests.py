from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

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