from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest
from django.shortcuts import redirect


class NotLoggedIn(AccessMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:profile')
        return super().dispatch(request, *args, **kwargs)
