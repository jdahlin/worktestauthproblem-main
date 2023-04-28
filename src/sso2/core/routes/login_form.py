from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, PasswordInput, TextInput
from django.shortcuts import resolve_url
from django.urls import reverse
from two_factor.forms import AuthenticationTokenForm, BackupTokenForm
from two_factor.views.core import LoginView

from sso2.core.models.tenant_model import Tenant


class NewAuthenticationForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(
            attrs={
                "placeholder": "Enter your username",
                "icon": "fa-user",
                "autofocus": "1",
                "autocomplete": "username",
            },
        ),
    )
    password = CharField(
        widget=PasswordInput(
            attrs={
                "placeholder": "••••••••••••••••",
                "icon": "fa-lock",
                "autocomplete": "current-password",
            },
        ),
    )

    def clean(self) -> dict[str, str]:
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        assert self.request is not None
        tenant_id = self.request.path.split("/")[2]
        tenant = Tenant.get_or_404(tenant_id=tenant_id)
        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
                tenant=tenant,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class NewLoginView(LoginView):  # type: ignore[misc]
    template_name = "login.html"
    form_list = (
        ("auth", NewAuthenticationForm),
        ("token", AuthenticationTokenForm),
        ("backup", BackupTokenForm),
    )

    def get_success_url(self) -> str:
        url = self.get_redirect_url()
        tenant_id = self.request.path.split("/")[2]
        tenant = Tenant.get_or_404(tenant_id=tenant_id)
        return url or resolve_url(reverse("home", kwargs={"tenant_id": tenant.id}))
