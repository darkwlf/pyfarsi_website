from django.http import HttpRequest
from django.shortcuts import redirect


def not_logged_in(func):
    def check(request: HttpRequest, /, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:profile')
        return func(request, *args, **kwargs)

    return check
