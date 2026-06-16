from django.contrib import admin
from .models import PanelMember

@admin.register(PanelMember)
class PanelMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'panel_type', 'session', 'order')
    list_filter = ('panel_type', 'session')
    search_fields = ('user__full_name', 'user__email', 'designation')
    
    # This allows admins to drag/type numbers directly in the list view to reorder the panel!
    list_editable = ('order', 'panel_type') 
    
    # Turns the user selection into a fast search bar
    autocomplete_fields = ('user',)