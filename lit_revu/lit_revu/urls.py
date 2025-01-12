from django.contrib import admin
from django.urls import path
import reviews.views
import authentication.views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from authentication.forms import LoginForm, NewPasswordForm

urlpatterns = [
    # Authentication app
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("signup/", authentication.views.signup_page, name="signup"),
    path(
        "signup/done",
        authentication.views.signup_done,
        name="signup_done",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", authentication.views.profile_page, name="profile"),
    path(
        "profile/password_change/",
        PasswordChangeView.as_view(
            form_class=NewPasswordForm,
            template_name="authentication/password_change_form.html",
            success_url="profile/password_change/done",
        ),
        name="password_change",
    ),
    path(
        "profile/password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # Reviews app
    path("tickets/", reviews.views.ticket_list, name="ticket_list"),
    path("tickets/<int:ticket_id>/", reviews.views.ticket_detail, name="ticket_detail"),
]
