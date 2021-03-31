from django import forms

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
    # space_open = forms.BooleanField(label='Is the Location Open?')
