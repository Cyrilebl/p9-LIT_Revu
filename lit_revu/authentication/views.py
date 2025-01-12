from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from . import forms


def signup_page(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["signup_done"] = True
            return redirect("signup_done")
    return render(request, "authentication/signup.html", context={"form": form})


def signup_done(request):
    if request.session.get("signup_done"):
        del request.session["signup_done"]
        return render(request, "authentication/signup_done.html")
    return redirect("signup")


@login_required
def profile_page(request):
    return render(request, "authentication/profile.html")
