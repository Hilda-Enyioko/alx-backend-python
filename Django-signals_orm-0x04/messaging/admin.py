from django.contrib import admin
from .models import Message, MessageHistory, Notification, User

# Register your models here.
admin.site.register(Message)
admin.site.register(MessageHistory)
admin.site.register(Notification)
admin.site.register(User)