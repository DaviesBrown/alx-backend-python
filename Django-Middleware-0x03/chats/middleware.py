#!/usr/bin/env python3
import logging
from datetime import datetime, time
from rest_framework.response import Response
from django.http import HttpResponse

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

    class RestrictAccessByTimeMiddleware:
        """
        Middleware to restrict access to certain views based on the time of day.
        """
        def __init__(self, get_response):
            """Initialize the middleware with the get_response callable."""
            self.get_response = get_response

        def __call__(self, request):
            """Restrict access to certain views based on the time of day.
            """
            current_time = datetime.now().time()
            start_time = time(9, 0)
            end_time = time(18, 0)
            if start_time <= current_time <= end_time:
                return self.get_response(request)
            else:
                return Response("Access restricted to business hours (9 AM - 6 PM)", status=403)
