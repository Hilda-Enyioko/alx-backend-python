from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Message
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
    # Fetch threaded messages for the logged-in user
    messages = Message.objects.threaded_for_user(request.user)
    
    return render(request, 'messaging/inbox.html', {'messages': messages})