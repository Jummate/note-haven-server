from django.contrib import admin
from users.models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'created', 'modified', 'password', 'failed_attempts')  # Columns to display in the list view
    search_fields = ('email',)  # Add a search field for email
    ordering = ('created',)  # Order by the 'created' field
    # list_filter = ('is_active', 'is_admin')  # Add filters for is_active and is_admin fields


admin.site.register(CustomUser, CustomUserAdmin)