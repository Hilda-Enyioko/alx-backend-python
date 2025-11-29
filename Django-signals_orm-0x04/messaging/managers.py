from django.db import models

"""
UnreadMessageManager: A custom ORM manager to filter unread messages for a specific user.
"""
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
            .select_related('sender')
            .only('id', 'sender', 'content', 'timestamp', 'read', 'parent_message')
        )
