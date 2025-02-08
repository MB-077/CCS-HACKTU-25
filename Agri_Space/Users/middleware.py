from .models import TokenUsageLog, Account
from rest_framework.authtoken.models import Token

# Middleware to log token usage
class TokenUsageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, 'auth') and isinstance(request.user, Account) and request.auth and Token.objects.filter(key=request.auth.key).exists():
            TokenUsageLog.objects.create(
                token=request.auth,
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                path=request.path,
            )

        return response