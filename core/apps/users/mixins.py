"""Mixins of the users' app."""

from threading import Thread

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import TokenGenerator


class OnlyUnauthenticatedMixin(AccessMixin):
    """Mixin to restrict access to views only for unauthenticated users."""

    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users to home page."""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)  # type: ignore


class EmailMixin:
    """Email Mixin."""

    def send_activation_email(self, request, user):
        """Start a thread for sending activation email."""
        thread = Thread(target=self.__send_activation_email, args=(request, user))
        thread.start()

    @staticmethod
    def __send_activation_email(request, user):
        """Send activation email."""
        html_message = render_to_string('accounts/registration/account_activation_email.html', {
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': TokenGenerator.make_token(user),
        })
        send_mail(
            subject='Activate your account',
            message='Thank you for registering an account with us!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message
        )
