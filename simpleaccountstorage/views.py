from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie


class CsrfTokenView(View):
    """
    This endpoint provided a way for set the CSRF token when it's not
    already set.
    """
    @ensure_csrf_cookie
    def get(self, request, *args, **kwargs):
        # All the work is made automatically by the CsrfViewMiddleware.
        # Just retrurn an empty JSON response.
        return JsonResponse({})