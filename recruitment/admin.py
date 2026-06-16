from django.contrib import admin
from .models import RecruitmentSettings, RecruitmentApplication

@admin.register(RecruitmentSettings)
class RecruitmentSettingsAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'is_open', 'application_fee', 'deadline')
    list_filter = ('is_open',)
    # Makes the is_open toggle clickable directly from the list view!
    list_editable = ('is_open',) 


@admin.register(RecruitmentApplication)
class RecruitmentApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'department', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'department', 'session', 'created_at')
    search_fields = ('full_name', 'email', 'student_id', 'transaction_id', 'phone')
    
    # Keep sensitive payment data read-only to prevent tampering
    readonly_fields = ('transaction_id', 'payment_response', 'pdf_url', 'created_at')
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('University Info', {
            'fields': ('student_id', 'department', 'session', 'hall')
        }),
        ('Application Data', {
            'fields': ('skills', 'motivation', 'github', 'linkedin', 'portfolio')
        }),
        ('Payment Details', {
            'fields': ('payment_status', 'transaction_id', 'payment_response', 'pdf_url')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    # Custom Actions for the Admin Panel
    actions = ['mark_as_paid', 'mark_as_failed']

    @admin.action(description='Mark selected applications as PAID')
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payment_status='PAID')
        self.message_user(request, f'{updated} applications manually marked as PAID.')

    @admin.action(description='Mark selected applications as FAILED')
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(payment_status='FAILED')
        self.message_user(request, f'{updated} applications marked as FAILED.')