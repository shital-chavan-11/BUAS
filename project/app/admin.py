from django.contrib import admin
from .models import CustomUser, Profile

# Inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile  # Reference the Profile model
    fields = (
        'date_of_birth',
        'qualification',
        'reading_preferences',
        'address',
        'contact_no',
        'document',
        'profile_picture',
    )
    extra = 0  # Do not show empty forms for new profiles

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')  # Displayed fields in the list view
    search_fields = ('username', 'email', 'first_name', 'last_name', 'contact_no')  # Enable search
    list_filter = ('qualification', 'date_of_birth')  # Filters in the sidebar
    ordering = ('username',)  # Default ordering

    # Include the ProfileInline in the admin view for CustomUser
    inlines = [ProfileInline]

# Register the CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)
