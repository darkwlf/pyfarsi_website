from django.contrib.auth.decorators import login_required as original_login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from ipware import get_client_ip


def not_logged_in(func):
    def check(request: HttpRequest, /, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:profile')
        return func(request, *args, **kwargs)

    return check


@original_login_required
def login_required(func):
    def check(request: HttpRequest, /, *args, **kwargs):
        request.user.ip = get_client_ip(request)[0]
        request.user.save()
        return func(request, *args, **kwargs)

    return check
