from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

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


class Space(models.Model):
    space_name = models.CharField(max_length=500)
    space_description = models.CharField(max_length=1000)
    space_max_capacity = models.IntegerField()
    space_address1 = models.CharField(max_length=1024)
    space_address2 = models.CharField(max_length=1024, default="")
    space_zip_code = models.CharField(max_length=5)
    space_city = models.CharField(max_length=1024)
    space_state = models.CharField(max_length=50)
    space_country = models.CharField(max_length=1024)
    space_noise_level_allowed = models.IntegerField()
    space_noise_level = models.IntegerField()
    space_wifi = models.BooleanField()
    space_restrooms = models.BooleanField()
    space_food_drink = models.BooleanField()
    space_open = models.BooleanField(default=True)
    space_owner = models.ForeignKey('User', on_delete=models.CASCADE, default=None, null=True)
    space_tags = TaggableManager(blank=True)

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

    def owner_str(self):
        return self.space_owner.username

    def open_str(self):
        if self.space_open:
            return "This location is open"
        else:
            return "This location is closed"

    def address_str(self):
        if self.space_address2:
            address = "{} {}, {}, {} {}, {}".format(self.space_address1, self.space_address2, self.space_city,
                                                    self.space_state, self.space_zip_code, self.space_country)
        else:
            address = "{}, {}, {} {}, {}".format(self.space_address1, self.space_city,
                                                 self.space_state, self.space_zip_code, self.space_country)
        return address

class SpaceDateTime(models.Model):
    # Switch to char if this does not work
    space_date = models.CharField(max_length=100, default='EMPTY')
    space_start_time = models.CharField(max_length=100, default='EMPTY')
    space_end_time = models.CharField(max_length=100, default='EMPTY')
    # This should auto-close after the date listed or if the proprietor decides to manually close a space
    space_dt_closed = models.BooleanField(default=False)
    space_dt_reserved = models.BooleanField(default=False)
    # Value needs to only be non-empty if reserved = true -> covered in a later story for client side reservation
    space_dt_reserved_by = models.CharField(max_length=1000, default='No User')
    space_id = models.ForeignKey('Space', on_delete=models.CASCADE, default=None, null=True)

    # all the to string methods all the fields in the model
    def s_date_str(self):
        return self.space_date

    def s_start_str(self):
        return self.space_start_time

    def s_end_str(self):
        return self.space_end_time

    # A time/date slot for a space can be 'open' and reserved simultaneously. Open only means that it is active in use.
    def s_dt_closed_str(self):
        if self.space_dt_closed:
            return "The listed date/time has passed and this space opening is now closed."
        else:
            return "The listed date/time has not yet passed for this space opening, still open/active in use."

    def s_dt_reserved_str(self):
        if self.space_dt_reserved:
            return "This space is reserved!"
        else:
            return "This space has not been reserved yet."

    def s_dt_reserved_by_str(self):
        return self.space_dt_reserved_by

    def s_space_id(self):
        location = self.space_id.space_name
        return "This is an availability time for the following space: {}".format(location)

