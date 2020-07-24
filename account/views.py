from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .decorators import not_logged_in
from .forms import Register
from django.shortcuts import render, redirect


class Login(auth_views.LoginView):
    template_name = 'account/login.html'
    success_url_allowed_hosts = settings.ALLOWED_HOSTS
    redirect_authenticated_user = True


class Logout(LoginRequiredMixin, auth_views.LogoutView):
    redirect_field_name = None
    template_name = 'account/logout.html'

    
class PasswordReset(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = 'accounts:password_reset_done'
    email_template_name = 'accounts/password_reset_email.html'


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'account/reset_done.html'


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = 'accounts:password_reset_complete'


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


@not_logged_in
def register(request):
    context = dict()
    if request.method == 'POST':
        context['form'] = Register(request.POST)
        if context['form'].is_valid():
            temp_user = context['form'].save(False)
            temp_user.is_active = True
            temp_user.save()
            return redirect('account:login')
    else:
        context['form'] = Register()
    return render(request, 'account/register.html', context)
