from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Profile  # Adjust this according to your model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile_picture', 'address', 'document_upload')


from .models import Profile  # Adjust this according to your model

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'qualification', 'reading_preferences', 'document']  # Include any other fields you need
