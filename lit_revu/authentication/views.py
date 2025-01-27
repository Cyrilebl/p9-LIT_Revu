from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from . import forms


def signup_page(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Félicitations, votre compte a été créé avec succès."
            )
            return redirect("login")
    return render(request, "authentication/signup.html", context={"form": form})


@login_required
def profile_page(request):
    return render(request, "authentication/profile.html")


@login_required
def custom_password_change_view(request):
    form = forms.NewPasswordForm(request.user)
    if request.method == "POST":
        form = forms.NewPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Votre mot de passe a été changé avec succès.")
            return redirect("profile")
    return render(
        request, "authentication/password_change.html", context={"form": form}
    )
