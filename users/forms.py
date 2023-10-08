"""
from django.forms import ModelForm
from users.models import User

class SignupForm(ModelForm):
    
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password"]
"""