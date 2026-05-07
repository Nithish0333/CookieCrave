from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Determine which fields are displayed on the list view
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login', 'date_joined')
    
    # Add filters to the right sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    # Add search capability
    search_fields = ('username', 'email')
    
    # Ensure they are ordered properly
    ordering = ('-date_joined',)

# Register the model with the customized ModelAdmin
admin.site.register(User, CustomUserAdmin)
