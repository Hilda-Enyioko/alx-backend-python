from django.db import models

# Create your models here.

"""
User model: A simple model to represent users in the messaging app.
"""
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

"""
Message model: A simple model to represent messages in the messaging app.
"""
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Parent message for threading
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    # ORM managers
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
    
    
    # Recursive method to fetch all replies for this message
    def get_thread(self):
        thread = []
        def _get_replies(message):
            for reply in message.replies.all():
                thread.append(reply)
                _get_replies(reply)
        _get_replies(self)
        return thread


"""
MessageHistory model: A model to keep track of message edits.
"""
class MessageHistory(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, related_name='edited_histories', on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"
  
"""
Notification model: A model to represent notifications related to messages.
"""
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about Message {self.message.id}"