from django.contrib import admin
from .models import Ticket, TicketUpdate

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "created_by", "assigned_to", "created_at")
    list_filter = ("status", "created_at",)
    search_fields = ("title", "description")

@admin.register(TicketUpdate)
class TicketUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "updated_by", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("update_text",)
