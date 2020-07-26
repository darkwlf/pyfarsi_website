from django.contrib.auth import views as auth_views
from utils.mixins import LoginRequired
from utils.decorators import not_logged_in
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from . import models
from .forms import Register


class Login(auth_views.LoginView):
    template_name = 'account/login.html'
    success_url_allowed_hosts = settings.ALLOWED_HOSTS
    redirect_authenticated_user = True


class Logout(LoginRequired, auth_views.LogoutView):
    redirect_field_name = None
    template_name = 'account/logout.html'


class PasswordReset(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = 'account:password_reset_done'
    email_template_name = 'account/password_reset_email.html'


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'account/reset_done.html'


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = 'account:password_reset_complete'


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class RegisterView(CreateView):
    form_class = Register
    success_url = 'account:register_complete'

    def form_valid(self, form):
        temp_user = form.save(False)
        temp_user.set_password(temp_user.password)
        temp_user.save()
        return redirect(self.get_success_url)


@not_logged_in
def register_complete(request):
    return render(request, 'account/register_complete.html')


def verify_email(request, key):
    user = get_object_or_404(models.Validation, key=key, user__is_active=False).user
    user.is_active = True
    user.save()
    return render(request, 'account/verify_email.html')
