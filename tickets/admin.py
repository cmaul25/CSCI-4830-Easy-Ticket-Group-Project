from django.contrib import admin

from .models import Ticket, TicketUpdate, UserProfile


class TicketUpdateInline(admin.TabularInline):
    model = TicketUpdate
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    inlines = [TicketUpdateInline]


@admin.register(TicketUpdate)
class TicketUpdateAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'updated_by', 'timestamp')
    search_fields = ('ticket__title', 'update_text', 'updated_by__username')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)