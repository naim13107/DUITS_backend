from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_published')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'location', 'description')
    
    # Allows admins to check/uncheck the published box directly from the main table
    list_editable = ('is_published',)
    
    # Custom Bulk Actions
    actions = ['publish_events', 'unpublish_events']

    @admin.action(description='Publish selected events')
    def publish_events(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} events successfully published.')

    @admin.action(description='Unpublish selected events')
    def unpublish_events(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} events successfully unpublished.')