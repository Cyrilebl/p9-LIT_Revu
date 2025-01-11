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
from authentication.forms import CustomLoginForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=CustomLoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("tickets/", reviews.views.ticket_list, name="ticket-list"),
    path("tickets/<int:ticket_id>/", reviews.views.ticket_detail, name="ticket-detail"),
]
