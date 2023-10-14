"""
from django.forms import ModelForm
from users.models import User

class SignupForm(ModelForm):
    
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password"]
"""
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'city', 'date_of_birth']
