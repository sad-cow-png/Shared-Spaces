from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


# Saves user as a proprietor
# Right now the client/props seem similiar, but later
# we may want different forms for different types of users
# (maybe we want the prop form to ask optionally for expected number of spaces)
class ClientSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

