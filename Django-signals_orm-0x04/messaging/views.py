from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Message
from .managers import UnreadMessagesManager
# Create your views here.

"""
Delete_User view: A view for users to delete themselves safely
Automatically remove all messages, notifications, and message histories for a user when they delete their account.
"""
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        
    return redirect('/')

"""
Inbox view: A view to display threaded messages for the logged-in user.
"""
@login_required
def inbox(request):
    
    # Fetch messages where user is either sender or receiver
    messages = (
        Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    ).filter(parent_message__isnull=True)  # Only top-level messages
    messages = messages.select_related(
        'sender', 'receiver'
        ).prefetch_related(
        'replies__sender', 'replies__receiver', 'replies__replies'
    ).distinct()

    # Build threaded structure for template
    threaded_messages = []
    for msg in messages:
        thread = [msg] + msg.get_thread()
        threaded_messages.append(thread)

    return render(request, 'messaging/inbox.html', {'threaded_messages': threaded_messages})

@login_required
def unread_inbox(request):
    user = request.user
    messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp', 'read', 'parent_message')

    return render(request, 'messaging/unread_inbox.html', {'messages': messages})

@cache_page(60)
@login_required
def cached_inbox(request):
    user = request.user

    # Fetch threaded messages
    messages = (
        Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
    ).filter(parent_message__isnull=True)
    messages = messages.select_related('sender', 'receiver').prefetch_related(
        'replies__sender', 'replies__receiver', 'replies__replies'
    ).distinct()

    # Build threaded structure for template
    threaded_messages = []
    for msg in messages:
        thread = [msg] + msg.get_thread()
        threaded_messages.append(thread)

    return render(request, 'messaging/inbox.html', {'threaded_messages': threaded_messages})