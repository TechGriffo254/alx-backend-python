"""
Custom middleware for the Django Messaging App.

This module contains middleware classes for:
1. Logging user requests
2. Restricting access by time
3. Rate limiting messages by IP
4. Enforcing role-based permissions
"""

import logging
from datetime import datetime, time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict
from time import time as current_time

# Configure logger
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log each user's requests to a file.
    
    Logs the following information:
    - Timestamp
    - User (username or 'Anonymous')
    - Request path
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
        
        # Configure file logger
        file_handler = logging.FileHandler('requests.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        
        # Get or create logger
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers and add file handler
        self.logger.handlers = []
        self.logger.addHandler(file_handler)
    
    def __call__(self, request):
        """Process the request and log information."""
        # Get user information
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Log request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """
    Middleware to restrict access to the messaging app during certain hours.
    
    Access is denied outside the hours of 9 AM to 6 PM.
    Returns 403 Forbidden error if accessed outside allowed hours.
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
        self.start_time = time(9, 0)  # 9:00 AM
        self.end_time = time(18, 0)   # 6:00 PM (6 PM)
    
    def __call__(self, request):
        """Check if current time is within allowed hours."""
        # Get current time
        current_hour = datetime.now().time()
        
        # Check if current time is outside allowed hours
        if not (self.start_time <= current_hour <= self.end_time):
            return JsonResponse({
                'error': 'Access denied',
                'message': 'Chat access is restricted to 9:00 AM - 6:00 PM only.',
                'current_time': datetime.now().strftime('%H:%M:%S'),
                'allowed_hours': '09:00 AM - 06:00 PM'
            }, status=403)
        
        # Process the request if within allowed hours
        response = self.get_response(request)
        
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware to limit the number of chat messages a user can send within a time window.
    
    Implements rate limiting based on IP address:
    - Maximum 5 messages per minute per IP address
    - Tracks POST requests to message endpoints
    - Returns 429 Too Many Requests if limit exceeded
    """
    
    # Class-level storage for request tracking
    # Format: {ip_address: [(timestamp1, request_count), (timestamp2, request_count), ...]}
    request_tracking = defaultdict(list)
    
    # Rate limit configuration
    MAX_REQUESTS = 5  # Maximum number of requests
    TIME_WINDOW = 60  # Time window in seconds (1 minute)
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Track and limit POST requests from each IP address."""
        # Only track POST requests (messages)
        if request.method == 'POST':
            # Get client IP address
            ip_address = self.get_client_ip(request)
            
            # Get current timestamp
            now = current_time()
            
            # Clean up old entries outside the time window
            self.cleanup_old_entries(ip_address, now)
            
            # Check if user has exceeded the rate limit
            if self.is_rate_limited(ip_address, now):
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'You can only send {self.MAX_REQUESTS} messages per minute. Please try again later.',
                    'retry_after': '60 seconds'
                }, status=429)
            
            # Add current request to tracking
            self.request_tracking[ip_address].append(now)
        
        # Process the request
        response = self.get_response(request)
        
        return response
    
    def get_client_ip(self, request):
        """Extract the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def cleanup_old_entries(self, ip_address, current_timestamp):
        """Remove entries older than the time window."""
        if ip_address in self.request_tracking:
            # Keep only entries within the time window
            cutoff_time = current_timestamp - self.TIME_WINDOW
            self.request_tracking[ip_address] = [
                timestamp for timestamp in self.request_tracking[ip_address]
                if timestamp > cutoff_time
            ]
    
    def is_rate_limited(self, ip_address, current_timestamp):
        """Check if the IP address has exceeded the rate limit."""
        if ip_address not in self.request_tracking:
            return False
        
        # Count requests within the time window
        request_count = len(self.request_tracking[ip_address])
        
        return request_count >= self.MAX_REQUESTS


class RolepermissionMiddleware(MiddlewareMixin):
    """
    Middleware to enforce role-based permissions.
    
    Checks if the user has admin or moderator role before allowing access.
    Returns 403 Forbidden if user doesn't have required permissions.
    """
    
    # Paths that require admin/moderator role
    PROTECTED_PATHS = [
        '/api/users/',
        '/api/conversations/',
        '/api/messages/',
    ]
    
    # Allowed roles
    ALLOWED_ROLES = ['admin', 'moderator']
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Check user role before allowing access to protected paths."""
        # Check if the request path requires role checking
        if self.is_protected_path(request.path):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'message': 'You must be logged in to access this resource.'
                }, status=401)
            
            # Check if user has the required role
            user_role = getattr(request.user, 'role', None)
            
            if user_role not in self.ALLOWED_ROLES:
                return JsonResponse({
                    'error': 'Permission denied',
                    'message': 'Access restricted to admin and moderator roles only.',
                    'your_role': user_role or 'guest',
                    'required_roles': self.ALLOWED_ROLES
                }, status=403)
        
        # Process the request
        response = self.get_response(request)
        
        return response
    
    def is_protected_path(self, path):
        """Check if the path requires role-based protection."""
        # Check if path starts with any protected path
        for protected_path in self.PROTECTED_PATHS:
            if path.startswith(protected_path):
                return True
        return False
