from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpRequest
from ipware import get_client_ip
from django.shortcuts import redirect
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator


class LoginRequired(LoginRequiredMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.ip = get_client_ip(request)[0]
            request.user.save()
        return super().dispatch(request, *args, **kwargs)


class NotLoggedIn(AccessMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:profile')
        return super().dispatch(request, *args, **kwargs)
