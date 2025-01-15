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
from django.conf import settings
from django.conf.urls.static import static


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
            success_url="done/",
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
    # Create
    path("tickets/new/", reviews.views.ticket_create, name="ticket_create"),
    path(
        "tickets/review/new/<int:ticket_id>/",
        reviews.views.review_create,
        name="review_create",
    ),
    # Read
    path("tickets/", reviews.views.ticket_list, name="ticket_list"),
    path(
        "tickets/<int:ticket_id>/", reviews.views.ticket_content, name="ticket_content"
    ),
    # Update
    path(
        "tickets/<int:ticket_id>/edit/",
        reviews.views.ticket_update,
        name="ticket_update",
    ),
    # Delete
    path(
        "tickets/<int:ticket_id>/delete/",
        reviews.views.ticket_delete,
        name="ticket_delete",
    ),
    # User posts
    path("tickets/<str:username>/", reviews.views.user_posts, name="user_posts"),
    # User followers / Read, Create, Delete
    path("follow/<str:username>/", reviews.views.user_followers, name="user_followers"),
    path(
        "follow/<str:username>/delete/<int:follow_id>",
        reviews.views.user_followers_delete,
        name="user_followers_delete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
