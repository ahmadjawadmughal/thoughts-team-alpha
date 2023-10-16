
from django import forms
from .models import Thought


class Thought_ShareForm(forms.Form):
    username =  forms.CharField(label="username", required=True)
    thought = forms.CharField(label="thought", required=True)