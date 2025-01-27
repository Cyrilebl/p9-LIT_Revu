from django.contrib import admin
from django.urls import path
import reviews.views
import authentication.views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
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
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", authentication.views.profile_page, name="profile"),
    path(
        "profile/password_change/",
        authentication.views.custom_password_change_view,
        name="password_change",
    ),
    # Tickets
    path("ticket/new/", reviews.views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/", reviews.views.ticket_content, name="ticket"),
    path(
        "tickets/<int:ticket_id>/edit/",
        reviews.views.ticket_update,
        name="ticket_update",
    ),
    path(
        "tickets/<int:ticket_id>/delete/",
        reviews.views.ticket_delete,
        name="ticket_delete",
    ),
    # Reviews
    path(
        "tickets/<int:ticket_id>/review/new/",
        reviews.views.review_create,
        name="review_create",
    ),
    path(
        "reviews/<int:review_id>/edit/",
        reviews.views.review_update,
        name="review_update",
    ),
    path(
        "reviews/<int:review_id>/delete/",
        reviews.views.review_delete,
        name="review_delete",
    ),
    # Followers
    path("followers/", reviews.views.user_followers, name="user_followers"),
    path(
        "followers/<int:follow_id>/delete/",
        reviews.views.user_followers_delete,
        name="user_followers_delete",
    ),
    # User tickets
    path("home/", reviews.views.ticket_list, name="home"),
    path("my-tickets/", reviews.views.user_tickets, name="user_tickets"),
    # Tickets and Reviews
    path("thread/new/", reviews.views.ticket_and_review_create, name="thread_create"),
    # Ticket or Tickets and Reviews
    path("post/type/", reviews.views.post_or_thread, name="post_or_thread"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
