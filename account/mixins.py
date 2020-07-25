from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from ipware import get_client_ip


class LoginRequired(LoginRequiredMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.ip = get_client_ip(request)[0]
            request.user.save()
        super().dispatch(request, *args, **kwargs)
