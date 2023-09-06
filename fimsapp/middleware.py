from django.contrib.sites.models import Site

from .jwtauth import JWTAuthentication


class AccountMiddleware(object):
    domain = Site.objects.get_current().domain

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.account, request.member = None, None

        if not request.user.is_authenticated:
            JWTAuthentication().authenticate(request)

        if (not request.user) or (not request.user.is_authenticated):
            response = self.get_response(request)
            return response

        response = self.get_response(request)
        return response
