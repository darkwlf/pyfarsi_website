from django.http import HttpRequest
from ipware import get_client_ip


class SaveIP:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated:
            request.user.ip = get_client_ip(request)[0]
            request.user.save()
            return self.get_response(request)
