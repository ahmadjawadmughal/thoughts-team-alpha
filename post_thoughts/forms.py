
from django import forms 
from post_thoughts.models import Thought
from users.models import User

class Thought_ShareForm(forms.Form):
    shared_with = forms.ModelMultipleChoiceField(queryset=User.objects.all())
