import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse
import time


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging to write to requests.log
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s",
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        # Process the request and return the response
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current hour (24-hour format)
        current_hour = datetime.now().hour

        # Define restricted hours (before 9 AM or after 6 PM)
        if current_hour < 9 or current_hour >= 18:
            return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Access to the messaging app is restricted between 6 PM and 9 AM.</p>")

        # Continue processing the request
        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track message counts and timestamps for each IP
        self.ip_data = {}
        # Offensive words list
        self.offensive_words = ["badword1", "badword2", "badword3"]

    def __call__(self, request):
        # Check if the request is a POST request for messages
        if request.method == "POST" and "/chat/" in request.path:
            # Get the user's IP address
            ip_address = self.get_client_ip(request)
            current_time = time.time()

            # Initialize or update IP tracking data
            if ip_address not in self.ip_data:
                self.ip_data[ip_address] = {"count": 0, "start_time": current_time}

            # Get the time window and message count for the IP
            time_window = 60  # 1 minute
            message_limit = 5
            ip_info = self.ip_data[ip_address]

            # Reset count if the time window has elapsed
            if current_time - ip_info["start_time"] > time_window:
                ip_info["count"] = 0
                ip_info["start_time"] = current_time

            # Increment the message count
            ip_info["count"] += 1

            # Block further messages if the limit is exceeded
            if ip_info["count"] > message_limit:
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait a minute before sending more messages."},
                    status=429,
                )

            # Check for offensive language in the message content
            message = request.POST.get("message", "").lower()
            if any(word in message for word in self.offensive_words):
                return JsonResponse(
                    {"error": "Your message contains offensive language and cannot be sent."},
                    status=400,
                )

        # Process the request if no limits are exceeded or offensive content detected
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Retrieve the client IP address from the request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and has a role
        if request.user.is_authenticated:
            # Get the user's role (this assumes you have a custom user model with a 'role' field)
            user_role = request.user.role

            # Define allowed roles
            allowed_roles = ['admin', 'moderator']

            # Check if the user has a valid role
            if user_role not in allowed_roles:
                return JsonResponse(
                    {"error": "You do not have permission to access this resource."},
                    status=403
                )
        else:
            # If the user is not authenticated, deny access
            return JsonResponse(
                {"error": "You must be logged in to access this resource."},
                status=401
            )

        # Proceed with the request if the user has the correct role
        response = self.get_response(request)
        return response