from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, CreateView

from .forms import LoginForm, RegisterUserForm, CustomPassRecMailForm, CustomSetPassForm
from .models import CustomUser
from .token import account_activation_token


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('accounts:email_confirmed')
    else:
        messages.add_message(request, messages.ERROR, 'Activation link is invalid!')
        return redirect('accounts:login')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class RegisterUserView(CreateView):
    success_url = reverse_lazy('accounts:r_mail_sent')
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        else:
            return super(RegisterUserView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Activate your Bitmenu account'
        message = render_to_string('accounts/account_activation_mail.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')

        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return super(RegisterUserView, self).form_valid(form)


class RegMailSentView(TemplateView):
    template_name = 'accounts/reg_mail_sent.html'


class EmailConfirmedView(TemplateView):
    template_name = 'accounts/email_confirmed.html'


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_mail.html'
    form_class = CustomPassRecMailForm


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class = CustomSetPassForm


class CustomPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
