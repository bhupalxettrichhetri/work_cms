from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.exceptions import PermissionDenied

ALLOWED_EMAILS = getattr(settings, "ALLOWED_EMAILS", [])

class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return True  # allow signup but we will restrict login access

    def authenticate(self, request, **credentials):
        return super().authenticate(request, **credentials)

    def pre_login(self, request, user, **kwargs):
        # This runs before login is finalized
        if user.email not in ALLOWED_EMAILS:
            raise PermissionDenied("message: unauthorized email")