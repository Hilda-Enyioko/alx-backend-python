from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

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

"""
A signal receiver that creates a MessageHistory instance
whenever a Message instance is updated (edited).
This uses the pre_save signal to log the old content of a message 
into a separate MessageHistory model before it’s updated.
"""
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    
    # Check if the message is being updated (not created)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass