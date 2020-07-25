from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .decorators import not_logged_in
from .forms import Register
from .tasks import remove_user


class Login(auth_views.LoginView):
    template_name = 'account/login.html'
    success_url_allowed_hosts = settings.ALLOWED_HOSTS
    redirect_authenticated_user = True


class Logout(LoginRequiredMixin, auth_views.LogoutView):
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


@not_logged_in
def register(request):
    context = dict()
    if request.method == 'POST':
        context['form'] = Register(request.POST)
        if context['form'].is_valid():
            temp_user = context['form'].save(False)
            temp_user.set_password(temp_user.password)
            temp_user.save()
            remove_user(temp_user.id)
            return redirect('account:login')
    else:
        context['form'] = Register()
    return render(request, 'account/register.html', context)


def verify_email(request, key):
    user = get_object_or_404(models.Validation, key=key, user__is_active=False).user
    user.is_active = True
    user.save()
    return render(request, 'account/verify_email.html')
