from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView

from .forms import UserRegisterForm


class UserLoginView(LoginView):
    """
    Final login view for the application.
    Uses a custom template and production-ready behavior.
    """

    template_name = "home.html"
    redirect_authenticated_user = True


class UserRegisterView(FormView):
    """
    User registration view.
    Creates an inactive user and sends an activation email.
    """

    template_name = "home.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        request = self.request

        activation_url = request.build_absolute_uri(
            reverse_lazy(
                "activate",
                kwargs={
                    "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
        )

        html_message = render_to_string(
            "users/email_activation.html",
            {
                "user": user,
                "activation_url": activation_url,
            },
        )

        email = EmailMultiAlternatives(
            subject="Potvrdenie registrácie",
            body="Aktivuj si účet kliknutím na odkaz v emaili.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        messages.success(
            request, "Registrácia prebehla úspešne. Skontroluj email a potvrď účet."
        )

        return super().form_valid(form)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(
                request, "Účet bol úspešne aktivovaný. Teraz sa môžeš prihlásiť."
            )
            return redirect("home")

        messages.error(
            request,
            "Aktivačný odkaz je neplatný alebo už bol použitý."
        )
        return redirect("home")
