from django.conf import settings

class AdminSessionMiddleware:
    """
    Uses a separate session cookie for the admin site
    so admin login doesn't affect front-end login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # swap session cookie
            original_cookie_name = settings.SESSION_COOKIE_NAME
            settings.SESSION_COOKIE_NAME = getattr(settings, 'ADMIN_SESSION_COOKIE_NAME', 'admin_session')
            response = self.get_response(request)
            settings.SESSION_COOKIE_NAME = original_cookie_name
            return response
        return self.get_response(request)
