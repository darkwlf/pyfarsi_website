from django.contrib.auth import views as auth_views
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Validation, User
from django.utils.html import strip_tags
from .tasks import remove_user
from .decorators import not_logged_in
from .mixins import NotLoggedIn
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .forms import Register, Profile


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


class RegisterView(NotLoggedIn, CreateView):
    form_class = Register
    template_name = 'account/register.html'
    success_url = 'account:register_complete'

    def form_valid(self, form):
        temp_user = form.save(False)
        temp_user.set_password(temp_user.password)
        temp_user.save()
        email_template = render_to_string(
            'account/email_validation.html',
            {
                'user': temp_user,
                'key': Validation.objects.create(user=temp_user).key,
                'base_domain': f'https://{settings.ALLOWED_HOSTS[0]}'
            }
        )
        send_mail(
            'فعال سازی حساب',
            strip_tags(email_template),
            settings.EMAIL_HOST_USER,
            (temp_user.email,),
            html_message=email_template
        )
        remove_user(temp_user.username)
        return redirect(self.success_url)


@not_logged_in
def register_complete(request):
    return render(request, 'account/register_complete.html')


def verify_email(request, key):
    user = get_object_or_404(models.Validation, key=key, user__is_active=False).user
    user.is_active = True
    user.save()
    return render(request, 'account/verify_email.html')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = Profile
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return self.request.user
