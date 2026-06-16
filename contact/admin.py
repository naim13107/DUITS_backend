from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    
    # Allow admins to mark messages as read directly from the list view
    list_editable = ('is_read',)
    
    # Make the actual message strictly read-only so it can't be altered
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    
    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description='Mark selected messages as Read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected messages as Unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)