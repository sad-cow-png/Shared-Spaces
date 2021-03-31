from django.test import TestCase
from .forms import CreateSpaceForm, Noise_Level_Choices
from .models import Space


# Tests will cover both newly entered form data and associated Create Spaces database
class CreateSpaceTests(TestCase):
    TestCase.default_data = {"space_name": 'TestName',
                             "space_description": 'Rand Description',
                             "space_max_capacity": 5,
                             "space_noise_level_allowed": [Noise_Level_Choices[0][0]],
                             "space_noise_level": [Noise_Level_Choices[1][0]],
                             "space_wifi": True,
                             "space_restrooms": False,
                             "space_food_drink": True}
    TestCase.test_form = CreateSpaceForm(data=TestCase.default_data)
    TestCase.test_form.is_valid()

    # Form entry accuracy tests
    def test_form_accuracy_name(self):
        # Creating a Test to check if the name is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_name'], 'TestName',
                         'space name not submitted correctly and in accurate location')

    def test_form_accuracy_description(self):
        # Creating a Test to check if the description is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_description'], 'Rand Description',
                         'space description not submitted correctly and in accurate location')

    def test_form_accuracy_capacity(self):
        # Creating a Test to check if the max capacity is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_max_capacity'], 5,
                         'space max capacity not submitted correctly and in accurate location')

    def test_form_accuracy_noise_allowed(self):
        # Creating a Test to check if the allowed noise level is saved same as the input from browser
        self.assertEqual(TestCase.test_form.cleaned_data.get('space_noise_level_allowed'), ['1'],
                         'space noise level allowed not submitted correctly and in accurate location')

    def test_form_accuracy_noise_level(self):
        # Creating a Test to check if the noise level is saved same as the input from browser
        self.assertEqual(TestCase.test_form.cleaned_data.get('space_noise_level'), ['2'],
                         'space noise level not submitted correctly and in accurate location')

    def test_form_accuracy_wifi(self):
        # Creating a Test to check if the wifi availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_wifi'], True,
                         'space wifi availability not submitted correctly and in accurate location')

    def test_form_accuracy_restroom(self):
        # Creating a Test to check if the restroom availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_restrooms'], False,
                         'space restroom availability not submitted correctly and in accurate location')

    def test_form_accuracy_fd(self):
        # Creating a Test to check if the food and drink availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_food_drink'], True,
                         'space food/drink availability not submitted correctly and in accurate location')

    # Tests that cover database accuracy once form is submitted
    # The following steps describe the order of steps for the rest of the data base accuracy tests.
    #   first save the data in to the database
    #   start by extracting the data from the form
    # Running tests to see accurate data made it's way to the database
    # while doing so check the string output as well
    # Tests to see if all the information from the string return is accurate
    def test_form_to_database_accuracy_name(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        # put the data into the space mode and create a new space model
        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # Test name
        self.assertEqual(test_space.name_str(), name, 'The location name was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy for space description
    def test_form_to_database_accuracy_description(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # test space description
        self.assertEqual(test_space.description_str(), description,
                         'The location description was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy for max capacity
    def test_form_to_database_accuracy_maxcap(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # test space max cap
        self.assertEqual(test_space.max_cap_str(), "This location has {} total spots open.".format(max_capacity),
                         'The location max capacity was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy for max noise allowed
    def test_form_to_database_accuracy_max_noise(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # test max noise allowed string
        self.assertEqual(test_space.noise_allowed_str(), "This location allows a max of {} noise level".format(
            Noise_Level_Choices[noise_level_allowed - 1][1]),
                         'The location allowed noise level was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy for noise level
    def test_form_to_database_accuracy_noise(self):
        # first save the data in to the database
        # start by extracting the data from the form
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        # put the data into the space mode and create a new space model
        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # noise test string
        self.assertEqual(test_space.noise_str(),
                         "This location has a noise level {} ".format(Noise_Level_Choices[noise_level - 1][1]),
                         'The location noise level was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy for restroom
    def test_form_to_database_accuracy_restroom(self):
        # first save the data in to the database
        # start by extracting the data from the form
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        # put the data into the space mode and create a new space model
        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # testing restroom string
        self.assertEqual(test_space.restroom_str(), "This place does not have restrooms.",
                         'The location restroom availability was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy for wifi
    def test_form_to_database_accuracy_wifi(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # testing wifi string
        self.assertEqual(test_space.wifi_str(), "This place has wifi.",
                         'The location wifi availability was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Tests that cover database accuracy of food and drink
    def test_form_to_database_accuracy_food_drink(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']

        # put the data into the space mode and create a new space model
        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink)

        # Submitting test form data to the create space database
        test_space.save()

        # testing food and drink string
        self.assertEqual(test_space.food_drink_str(), "This place has food and drink.",
                         'The location food and drink availability was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Selenium testing will be added later for testing front end to database
