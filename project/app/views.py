from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from .models import Profile  # Assuming you have a Profile model
from .forms import ProfileUpdateForm  # Make sure to create this form
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm 
from .models import Profile
# In app/views.py
from .forms import ProfileUpdateForm
import re

CustomUser = get_user_model()  # Ensure you are using the correct user model


def register_view(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        qualification = request.POST.get("qualification")
        reading_preferences = request.POST.get("reading_preferences")
        profile_picture = request.FILES.get("profile_picture")
        address = request.POST.get("address")
        document = request.FILES.get("document")  # Ensure the document is retrieved
        contact_no = request.POST.get("contact_no")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already taken!")
            return redirect('register')

        # Validate other fields (optional)
        if not validate_phone(contact_no):
            messages.error(request, "Invalid phone number!")
            return redirect('register')

        try:
            with transaction.atomic():  # Ensure all changes are made or none
                # Create the user
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )

                # Create a related profile for the user
                Profile.objects.create(
                    user=user,
                    date_of_birth=date_of_birth,
                    qualification=qualification,
                    reading_preferences=reading_preferences,
                    profile_picture=profile_picture,  # Assign profile picture if provided
                    document=document,  # Assign document if provided
                    address=address,  # Add address to the profile
                    contact_no=contact_no,  # Add contact number to the profile
                )

                messages.success(request, "Registration successful!")
                return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred during registration: {e}")
            return redirect('register')

    return render(request, 'register.html')


def validate_phone(phone):
    """Validate the phone number format (example: 10 digits)"""
    return re.match(r'^\d{10}$', phone) is not None

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to the dashboard after logging in
        else:
            messages.error(request, "Invalid credentials!")  # Show error on invalid login attempt

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, "Logout successful!")  # Set the logout message
    return redirect('login')  # Redirect to the login page


@login_required
def dashboard_view(request):
    user = request.user  # Get the logged-in user
    
    # Attempt to get the associated profile
    profile = Profile.objects.filter(user=user).first()  # Use filter().first() to avoid exceptions

    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile': profile,  # Add the profile object to the context
    }
    
    return render(request, 'dashboard.html', context)  # Make sure the templateturn render(request, 'dashboard.html', context)  # Pass context directly
@login_required
def profile_view(request):
    """Display the user's profile."""
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create the profile
    return render(request, 'profile.html', {'profile': profile})  # Pass profile to the template

@login_required
def update_profile(request):
    """Update the user's profile information."""
    # Ensure the profile exists, create if it does not
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the form changes
            messages.success(request, "Profile updated successfully!")  # Provide success message
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile for the user when the user is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user's profile when the user is saved."""
    instance.profile.save()