#!/usr/bin/env python3
from datetime import datetime
import logging

logger = logging.getLogger('middleware_logger')

class RequestLoggerMiddleware:
    """
    Middleware to log the request method and path.
    """

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Log the request method and path along with the user information."""
        response = self.get_response(request)
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return response
