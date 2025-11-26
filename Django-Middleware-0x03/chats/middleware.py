from datetime import datetime
import logging
from django.conf import settings
import os

# A middleware that logs each user’s requests to a file
# including the timestamp, user and the request path.

# The log file already exists inside the project directory
# This is where we will store our logs
log_file_path = os.path.join(settings.BASE_DIR, 'requests.log')

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = 'AnonymousUser'
        
        log_message = f"Date: {datetime.now()} - User: {user} - Request: {request.path}"
        logging.info(log_message)
        
        return self.get_response(request)
    

# A middleware that restricts access to messaging views during certain hours of the day
# deny access by returning an error 403 Forbidden

from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request_hour = datetime.now().hour
        
        # Allow access only between 6 AM and 9 PM
        if not (6 <= request_hour < 21):
            return HttpResponseForbidden("Chat access is restricted during this time.")
        
        return self.get_response(request)
    

# A middleware that blocks spam messages
# By limiting users to 5 messages sent per minute

from django.utils.timezone import now
from datetime import timedelta

class  OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_records = {}
        self.message_limit = 5
        self.time_window = timedelta(minutes=1)
        
    def __call__(self, request):
        if request.method == "POST":
            sender_ip = self.get_client_ip(request)
            current_time = now()
            
            if sender_ip not in self.message_records:
                self.message_records[sender_ip] = []
                
            # clean old timestamps outside the time_window
            self.message_records[sender_ip] = [timestamp for timestamp in self.message_records[sender_ip] if current_time - timestamp < self.time_window]
            
            # check if message limit has been reached
            if len(self.message_records[sender_ip]) >= self.message_limit:
                return HttpResponseForbidden(
                    "Message limit exceeded. You can only send 5 messages per minute."
                )
            
            # Add current timestamp
            self.message_records[sender_ip].append(current_time)
            
            return self.get_response(request)
        
        def get_client_ip(self, request):
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            
            if x_forwarded_for:
                return x_forwarded_for.split(",")[0].strip()
            
            return request.META.get("REMOTE_ADDR")