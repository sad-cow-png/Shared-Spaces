from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


# Saves user as a proprietor
class ProprietorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


