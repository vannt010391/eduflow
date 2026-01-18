"""
Custom middleware for EduFlow AI
"""
from django.conf import settings

# The session key used by Django's LocaleMiddleware
LANGUAGE_SESSION_KEY = '_language'


class ClearSessionLanguageMiddleware:
    """
    Middleware to ensure language is ONLY stored in cookie, not session.
    This prevents session from overriding cookie values.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear language from session if it exists
        # This forces Django to use cookie instead
        if hasattr(request, 'session') and LANGUAGE_SESSION_KEY in request.session:
            del request.session[LANGUAGE_SESSION_KEY]

        response = self.get_response(request)
        return response
