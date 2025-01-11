from django.contrib import admin
from .models import Ticket, Review, UserFollows
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["username", "email"]
    ordering = ["username"]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(UserFollows)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created")
    search_fields = ("title",)
    list_filter = ("time_created",)
    ordering = ("-time_created",)
