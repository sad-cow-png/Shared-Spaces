from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# This represents the multiple choice options for the noise level multiple choice fields.
Noise_Level_Choices = (
    ("1", "None"),
    ("2", "Faint"),
    ("3", "Moderate"),
    ("4", "Loud"),
    ("5", "Very Loud")
)


# For for creating the specific space and also to modify it.
class CreateSpaceForm(forms.Form):
    space_name = forms.CharField(label='Name of the Shared Space:', max_length=500, strip=True)
    space_description = forms.CharField(label='Description:', max_length=1000, strip=True)
    space_max_capacity = forms.IntegerField(label='Maximum Occupancy:', min_value=0)
    space_noise_level_allowed = forms.MultipleChoiceField(label='Noise level allowed:', choices=Noise_Level_Choices,
                                                          required=True)
    space_noise_level = forms.MultipleChoiceField(label='Noise level:', choices=Noise_Level_Choices, required=True)
    space_wifi = forms.BooleanField(label='Wifi Availability:', required=False)
    space_restrooms = forms.BooleanField(label='Restroom Availability:', required=False)
    space_food_drink = forms.BooleanField(label='Food or Drink Availability:', required=False)
    space_open = forms.BooleanField(label='Is the Location Open?', required=False)

    
# Used for proprietor sign up view
class ProprietorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        
        
# Saves user as a proprietor
# Right now the client/props seem similar, but later
# we may want different forms for different types of users
# (maybe we want the prop form to ask optionally for expected number of spaces)
class ClientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


# User will enter the date the space will be available and the start and end time
class SpaceTimes(forms.Form):
    date = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y'), required=True)
    time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
    time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
    closed = forms.BooleanField(label='Is this time currently available?', required=False)


class SearchBar(forms.Form):
    Search_Choices = (
        ('all', 'All'),
        ('space','Space Details'),
        ('user', 'User'),
        ('date', 'Date Available'),
    )
    query = forms.CharField(max_length=1000, strip=True)
    filters = forms.ChoiceField(choices=Search_Choices)
