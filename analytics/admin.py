from django.contrib import admin
from .models import SystemLog

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('action', 'details', 'user__email', 'ip_address')
    
    # Make EVERYTHING read-only
    readonly_fields = ('user', 'action', 'details', 'ip_address', 'timestamp')

    # Security: Disable the ability to add or delete logs through the admin panel
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False