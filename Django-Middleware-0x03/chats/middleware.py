# A middleware that logs each user’s requests to a file
# including the timestamp, user and the request path.

from datetime import datetime
import logging
from django.conf import settings
import os

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