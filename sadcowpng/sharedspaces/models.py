from django.db import models

# Create your models here.


# All information that will be sent to space
class Space(models.Model):
    space_name = models.CharField(max_length=500)
    space_description = models.CharField(max_length=1000)
    space_max_capacity = models.IntegerField()
    space_noise_level_allowed = models.CharField(max_length=50)
    space_noise_level = models.CharField(max_length=50)
    space_wifi = models.BooleanField()
    space_restrooms = models.BooleanField()
    space_food_drink = models.BooleanField()

    # Might want to create a string method for each data type
    def name_str(self):
        return self.space_name
