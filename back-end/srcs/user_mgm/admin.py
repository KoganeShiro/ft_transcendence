from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add custom fields to the admin panel
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('cover_photo', 'online', 'friends')}),
    )
