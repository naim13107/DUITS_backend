from django.contrib import admin
from .models import Category, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # This automatically types out the slug in the admin panel as you type the name
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 1. What columns to show in the list view
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    
    # 2. Add a filter sidebar on the right side
    list_filter = ('status', 'category', 'created_at')
    
    # 3. Add a search bar (Notice the double underscore to search by author's full name/email)
    search_fields = ('title', 'content', 'author__full_name', 'author__email', 'tags')
    
    # 4. Make dates read-only so admins can't accidentally change when it was published
    readonly_fields = ('created_at', 'updated_at')
    
    # 5. Makes the dropdowns searchable (Great for when you have hundreds of users)
    autocomplete_fields = ('author', 'category')

    # --- CUSTOM APPROVAL WORKFLOW ACTIONS ---
    actions = ['approve_articles', 'reject_articles']

    @admin.action(description='Approve selected articles')
    def approve_articles(self, request, queryset):
        # Updates the status of all selected checkboxes to APPROVED
        updated = queryset.update(status='APPROVED')
        # Shows a green success message at the top of the screen
        self.message_user(request, f'{updated} articles were successfully approved.')

    @admin.action(description='Reject selected articles')
    def reject_articles(self, request, queryset):
        # Updates the status of all selected checkboxes to REJECTED
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'{updated} articles were successfully rejected.')