from django.db import models
from .forms import Noise_Level_Choices


# All information that will be sent to space
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

    # Might want to create a string method for each data type
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
