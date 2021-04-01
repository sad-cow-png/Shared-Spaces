from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: make a directory to hold static data.
# This represents the multiple choice options for the noise level multiple choice fields.
Noise_Level_Choices = (
    ("1", "None"),
    ("2", "Faint"),
    ("3", "Moderate"),
    ("4", "Loud"),
    ("5", "Very Loud")
)

# Create user as a client or proprietor
class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_proprietor = models.BooleanField(default=False)


# This table or model will hold all the data that defines each of the spaces.
class Space(models.Model):
    space_name = models.CharField(max_length=500)
    space_description = models.CharField(max_length=1000)
    space_max_capacity = models.IntegerField()
    space_noise_level_allowed = models.IntegerField()
    space_noise_level = models.IntegerField()
    space_wifi = models.BooleanField()
    space_restrooms = models.BooleanField()
    space_food_drink = models.BooleanField()
    # space_open = models.BooleanField()

    # string methods for each of the different model fields
    def name_str(self):
        return self.space_name

    def description_str(self):
        return self.space_description

    def max_cap_str(self):
        return "This location has {} total spots open.".format(self.space_max_capacity)

    def noise_allowed_str(self):
        return "This location allows a max of {} noise level".format(
            Noise_Level_Choices[self.space_noise_level_allowed - 1][1])

    def noise_str(self):
        return "This location has a noise level {} ".format(
            Noise_Level_Choices[self.space_noise_level - 1][1])

    def wifi_str(self):
        if self.space_wifi:
            return "This place has wifi."
        else:
            return "This place does not have wifi."

    def restroom_str(self):
        if self.space_restrooms:
            return "This place has restrooms."
        else:
            return "This place does not have restrooms."

    def food_drink_str(self):
        if self.space_food_drink:
            return "This place has food and drink."
        else:
            return "This place does not have food and drink."

