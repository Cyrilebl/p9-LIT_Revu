from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )

    error_messages = {
        "invalid_login": "Nom d'utilisateur ou mot de passe incorrect.",
        "inactive": "Ce compte est inactif.",
    }


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Prénom"})
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nom"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe"})
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name")


class NewPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs.update(
            {"placeholder": "Ancien mot de passe"}
        )
        self.fields["new_password1"].widget.attrs.update(
            {"placeholder": "Nouveau mot de passe"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"placeholder": "Confirmation du mot de passe"}
        )
