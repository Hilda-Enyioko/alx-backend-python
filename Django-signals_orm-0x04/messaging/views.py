from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
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