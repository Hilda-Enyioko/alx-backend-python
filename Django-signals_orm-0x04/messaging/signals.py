from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

"""
A signal receiver that creates a Notification instance 
for the receiver of a message
whenever a new Message instance is created.
The created flag ensures the notification is only created once.
"""
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
