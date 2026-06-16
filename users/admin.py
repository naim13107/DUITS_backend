from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 1. The columns shown on the list view of all users
    list_display = ('email', 'full_name', 'role', 'student_id', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'is_verified')
    search_fields = ('email', 'full_name', 'student_id')
    ordering = ('email',)

    # 2. The layout when you click on a specific user to edit them (This caused your error!)
    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'profile_image', 'bio')}),
        ('University Info', {'fields': ('student_id', 'department', 'hall', 'session')}),
        ('Roles & Status', {'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Advanced Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}), 
        # Note: join_date is not here because auto_now_add fields cannot be edited in the admin panel by default.
    )

    # 3. The layout when you click "Add user" in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password', 'role', 'is_staff', 'is_superuser')}
        ),
    )

# Register your model and the updated admin class
admin.site.register(User, CustomUserAdmin)