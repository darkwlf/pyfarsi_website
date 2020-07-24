from django.contrib.auth.views import LoginView
from django.conf import settings


class Login(LoginView):
    template_name = 'account/login.html'
    success_url_allowed_hosts = settings.ALLOWED_HOSTS
