from django.contrib import admin
from .models import Ticket, Review, UserFollows

admin.site.register(Review)
admin.site.register(UserFollows)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created")
    search_fields = ("title",)
    list_filter = ("time_created",)
    ordering = ("-time_created",)
