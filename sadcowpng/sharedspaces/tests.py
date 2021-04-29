from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from django.test import TestCase
from django.urls import reverse
from .forms import CreateSpaceForm, Noise_Level_Choices, ProprietorSignUpForm, ClientSignUpForm, SpaceTimes
from .models import Space, User, SpaceDateTime
import datetime


# Testing for the client signup
class ClientSignUpTest(TestCase):

    def setUp(self):
        self.precount = User.objects.count()
        self.credentials = {
            'username': 'testyBoy',
            'password': 'SomeReallyGoodPassword1#'
        }
        User.objects.create_user(**self.credentials)
        self.assertTrue(User.objects.count(), self.precount + 1)
        # I think that every class is seperate, so we all
        # work with seperate data bases
        # therefore my count should be 1 (0 before, 1 now)

    def test_client_signup_page(self):
        response = self.client.get('/sign_up/client/')  # move to client sign up page
        self.assertEqual(response.status_code, 200)
        # 200 means good for some reason
        # below, we check if we got the correct html file from this page
        self.assertTemplateUsed(response, template_name='sharedspaces/client_sign_up.html')

    def test_client_signup_view(self):
        response = self.client.get(reverse('client_sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='sharedspaces/client_sign_up.html')

    def test_invalid_signups(self):
        invalid_data = [
            # username already exists bad
            {
                'data': {

                    'username': 'testyBoy',
                    'password1': 'SomeReallyGoodPassword1#',
                    'password2': 'SomeReallyGoodPassword1#',
                }
            },
            # password numeric
            {
                'data': {
                    'username': 'goodName',
                    'password1': '12345678',
                    'passwrod2': '12345678',
                }
            },
            # password too short
            {
                'data': {
                    'username': 'JobiKenobi',
                    'password1': 'pass',
                    'password2': 'pass',
                }
            },
            # password too common
            {
                'data': {
                    'username': 'MyGodIHateMyLife',
                    'password1': 'asdfghjkl',
                    'password2': 'asdfghjkl',
                }
            },

            # password doesn't match
            {
                'data': {
                    'username': 'SupidIdiot',
                    'password1': 'XhajJSkd45',
                    'password2': 'jahkHAWO34g',
                }
            },
            # that covers all the basis
        ]
        for invalid_users in invalid_data:
            form = ClientSignUpForm(data=invalid_users['data'])
            self.failIf(form.is_valid())

    def test_valid_client_signup(self):
        good_data = {
            'username': 'JobiBenKenobi',
            'password1': 'DisneyInfringementIsMyRight1@',
            'password2': 'DisneyInfringementIsMyRight1@',
        }

        response = self.client.post('/sign_up/client/', data=good_data)
        self.assertEqual(response.status_code, 302)
        # right now, we should have 2 more objects from start
        self.assertEqual(User.objects.count(), self.precount + 2)

        # find that user and check if he/she has is_client
        user = User.objects.get(username='JobiBenKenobi')
        self.assertEqual(user.is_client, True)
        # we may also want to check the user has is_prop false
        self.assertEqual(user.is_proprietor, False)
        self.assertRedirects(response, '/')


# Test proprietor signup with invalid and valid users
class ProprietorSignUpTest(TestCase):
    def setUp(self):
        # Used for existing user test
        self.credentials = {
            'username': 'test',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.credentials)
        self.assertTrue(User.objects.count(), 1)

    def test_signup_page(self):
        response = self.client.get('/sign_up/proprietor/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='sharedspaces/proprietor_signup.html')

    def test_signup_view(self):
        response = self.client.get(reverse('proprietor_sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='sharedspaces/proprietor_signup.html')

    def test_invalid_signup(self):
        invalid_data = [
            # username already exists
            {
                'data': {
                    'username': 'test',
                    'password1': '#zgsXJLY5jRb35j',
                    'password2': '#zgsXJLY5jRb35j',
                }
            },
            # password entirely numeric
            {
                'data': {
                    'username': 'john',
                    'password1': '1233556',
                    'password2': '1233556'
                }
            },
            # password too short
            {
                'data': {
                    'username': 'someone',
                    'password1': 'sdfg34',
                    'password2': 'sdfg34',
                }
            },

            # password too common
            {
                'data': {
                    'username': 'foo',
                    'password1': 'asdfghjkl',
                    'password2': 'asdfghjkl',
                }
            },

            # password doesn't match
            {
                'data': {
                    'username': 'foo2',
                    'password1': 'XhajJSkd45',
                    'password2': 'jahkHAWO34g',
                }
            },

        ]
        for invalid_users in invalid_data:
            form = ProprietorSignUpForm(data=invalid_users['data'])
            self.failIf(form.is_valid())

    def test_valid_signup(self):
        data = {
            'username': 'testuser2',
            'password1': 'XGAHvnd457',
            'password2': 'XGAHvnd457',
        }

        # Check form has correct fields
        response = self.client.get('/sign_up/proprietor/')
        self.assertContains(response, 'username')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')

        # Sign up with user data
        response = self.client.post('/sign_up/proprietor/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)

        # Check is_proprietor flag is set for user
        user = User.objects.get(username='testuser2')
        self.assertEqual(user.is_proprietor, True)

        self.assertRedirects(response, '/')


# Test login form and view
class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.credentials)
        user = User.objects.all()
        self.assertTrue(user.count(), 1)

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='sharedspaces/login.html')

    def test_login_fields(self):
        response = self.client.get('/login/')
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check if user is logged in
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_active)

        self.assertRedirects(response, '/account/')

    # Should redirect to login if accessing account page
    # while not logged in
    def test_not_logged_in(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/account/')


# Tests will cover both newly entered form data and associated Create Spaces database
class CreateSpaceTests(TestCase):
    TestCase.default_data = {"space_name": 'TestName',
                             "space_description": 'Rand Description',
                             "space_max_capacity": 5,
                             "space_noise_level_allowed": [Noise_Level_Choices[0][0]],
                             "space_noise_level": [Noise_Level_Choices[1][0]],
                             "space_wifi": True,
                             "space_restrooms": False,
                             "space_food_drink": True,
                             "space_open": True}
    TestCase.test_form = CreateSpaceForm(data=TestCase.default_data)
    TestCase.test_form.is_valid()

    # Form entry accuracy tests
    def test_form_accuracy_name(self):
        # Creating a Test to check if the name is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_name'], 'TestName',
                         'space name submitted correctly and in accurate location')

    def test_form_accuracy_description(self):
        # Creating a Test to check if the description is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_description'], 'Rand Description',
                         'space description submitted correctly and in accurate location')

    def test_form_accuracy_capacity(self):
        # Creating a Test to check if the max capacity is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_max_capacity'], 5,
                         'space max capacity submitted correctly and in accurate location')

    def test_form_accuracy_noise_allowed(self):
        # Creating a Test to check if the allowed noise level is saved same as the input from browser
        self.assertEqual(TestCase.test_form.cleaned_data.get('space_noise_level_allowed'), ['1'],
                         'space noise level allowed submitted correctly and in accurate location')

    def test_form_accuracy_noise_level(self):
        # Creating a Test to check if the noise level is saved same as the input from browser
        self.assertEqual(TestCase.test_form.cleaned_data.get('space_noise_level'), ['2'],
                         'space noise level submitted correctly and in accurate location')

    def test_form_accuracy_wifi(self):
        # Creating a Test to check if the wifi availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_wifi'], True,
                         'space wifi availability submitted correctly and in accurate location')

    def test_form_accuracy_restroom(self):
        # Creating a Test to check if the restroom availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_restrooms'], False,
                         'space restroom availability submitted correctly and in accurate location')

    def test_form_accuracy_fd(self):
        # Creating a Test to check if the food and drink availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_food_drink'], True,
                         'space food/drink availability submitted correctly and in accurate location')

    # added by Bishal ##################################################################################
    def test_form_accuracy_open(self):
        # Creating a Test to check if the food and drink availability is saved correctly
        self.assertEqual(TestCase.test_form.cleaned_data['space_food_drink'], True,
                         'Space availability submitted correctly and in accurate location')

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

    # added by Bishal ##################################################################################
    # Tests that cover database accuracy of food and drink
    def test_form_to_database_accuracy_space_open(self):
        name = TestCase.test_form.cleaned_data['space_name']
        description = TestCase.test_form.cleaned_data['space_description']
        max_capacity = TestCase.test_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_form.cleaned_data['space_wifi']
        restroom = TestCase.test_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_form.cleaned_data['space_food_drink']
        space_open = TestCase.test_form.cleaned_data['space_open']

        # put the data into the space mode and create a new space model
        test_space = Space(space_name=name,
                           space_description=description,
                           space_max_capacity=max_capacity,
                           space_noise_level_allowed=noise_level_allowed,
                           space_noise_level=noise_level,
                           space_wifi=wifi,
                           space_restrooms=restroom,
                           space_food_drink=food_drink,
                           space_open=space_open)

        # Submitting test form data to the create space database
        test_space.save()

        # testing food and drink string
        self.assertEqual(test_space.space_open, True,
                         'The space availability was stored in the database incorrectly.')

        # Deleting this entry from the database with it's unique ID number
        test_space.delete()

        # now check if it was deleted properly
        self.assertEqual(test_space.pk, None,
                         'The location was not deleted properly from the database.')

    # Selenium testing will be added later for testing front end to database


# added by Sharlet #################################################################################
class TestSpaceDateTime(TestCase):
    # Following date / time format specified in forms.py
    TestCase.default_data_date = {'date': '09/04/2021', 'time_start': '04:15', 'time_end': '05:15'}

    # First test just checks form accuracy
    TestCase.test_form_date = SpaceTimes(data=TestCase.default_data_date)
    TestCase.test_form_date.is_valid()

    TestCase.default_space_data = {"space_name": 'TestName',
                                   "space_description": 'Rand Description',
                                   "space_max_capacity": 5,
                                   "space_noise_level_allowed": [Noise_Level_Choices[0][0]],
                                   "space_noise_level": [Noise_Level_Choices[1][0]],
                                   "space_wifi": True,
                                   "space_restrooms": False,
                                   "space_food_drink": True}
    TestCase.test_space_form = CreateSpaceForm(data=TestCase.default_space_data)
    TestCase.test_space_form.is_valid()

    # added by Sharlet #################################################################################
    def test_form_accuracy_date(self):
        self.assertEqual(TestCase.test_form_date.cleaned_data['date'], '09/04/2021',
                         'space date was submitted correctly and stored accurately.')

    def test_form_accuracy_s_time(self):
        self.assertEqual(TestCase.test_form_date.cleaned_data['time_start'], datetime.time(4, 15),
                         'space start time was submitted correctly and stored accurately.')

    def test_form_accuracy_e_time(self):
        self.assertEqual(TestCase.test_form_date.cleaned_data['time_end'], datetime.time(5, 15),
                         'space end time was submitted correctly and stored accurately.')

    # added by Bishal ##################################################################################
    # Tests for model accuracy for all data types in model - would happen after a model object is saved.
    def test_date_time_model(self):
        # first create the space to access using fk
        name = TestCase.test_space_form.cleaned_data['space_name']
        description = TestCase.test_space_form.cleaned_data['space_description']
        max_capacity = TestCase.test_space_form.cleaned_data['space_max_capacity']
        noise_level_allowed = int(TestCase.test_space_form.cleaned_data["space_noise_level_allowed"][0])
        noise_level = int(TestCase.test_space_form.cleaned_data["space_noise_level"][0])
        wifi = TestCase.test_space_form.cleaned_data['space_wifi']
        restroom = TestCase.test_space_form.cleaned_data['space_restrooms']
        food_drink = TestCase.test_space_form.cleaned_data['space_food_drink']

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

        # now create and save the space data model
        space_date = TestCase.test_form_date.cleaned_data['date']
        space_start_time = TestCase.test_form_date.cleaned_data['time_start']
        space_end_time = TestCase.test_form_date.cleaned_data['time_end']
        space_id = test_space
        date_time = SpaceDateTime(space_date=space_date,
                                  space_start_time=space_start_time,
                                  space_end_time=space_end_time,
                                  space_id=space_id)
        date_time.save()

        # now try to access the name of the object
        self.assertEqual(date_time.s_date_str(), datetime.date(2021, 9, 4),
                         'Date is working properly.')
        self.assertEqual(date_time.s_start_str(), datetime.time(4, 15),
                         'Start time is working properly.')
        self.assertEqual(date_time.s_end_str(), datetime.time(5, 15),
                         'End time is working properly.')
        self.assertEqual(date_time.s_dt_closed_str(),
                         "The listed date/time has not yet passed for this space opening, still open/active in use.",
                         'Closed flag is working properly.')
        self.assertEqual(date_time.s_dt_reserved_str(),
                         "This space has not been reserved yet.",
                         'Reserved flag is working properly.')
        self.assertEqual(date_time.s_dt_reserved_by_str(), "No User",
                         'Date reserved by is working properly.')
        self.assertEqual(date_time.s_space_id(), "This is an availability time for the following space: TestName",
                         'Space foreign key is working properly.')
        # end ##########################################################################################################


# Creates client/proprietor users
# Can be used to create new users, reusable
# Run this before running decorator tests, if test users in
# ProprietorRequiredTest and SpaceOwnerTests are unchanged
class CreateUsers(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  # opens a webpage

        self.index_url = "http://127.0.0.1:8000"

        # Can be changed to create new users
        self.clientuser = 'spaceplease6'
        self.clientpw = 'jedwi5hak2'

        self.proprietoruser = 'proprietor5'
        self.proprietorpw = 'ajkDUI3#f'

        self.sp_name = "Space space"
        self.sp_desc = "This is a space for use."

    def proprietor_sign_up(self):
        driver = self.driver

        driver.get(self.index_url + '/sign_up/proprietor/')

        nameFieldelem = driver.find_element_by_name("username")
        passFieldElem = driver.find_element_by_name("password1")
        confirmPassElem = driver.find_element_by_name("password2")
        submitButtonElem = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        nameFieldelem.send_keys(self.proprietoruser)
        passFieldElem.send_keys(self.proprietorpw)
        confirmPassElem.send_keys(self.proprietorpw)
        ActionChains(driver).move_to_element(submitButtonElem).click(submitButtonElem).perform()
        submitButtonElem.send_keys(Keys.RETURN)

    def client_sign_up(self):
        driver = self.driver

        driver.get(self.index_url + '/sign_up/client/')

        nameFieldelem = driver.find_element_by_name("username")
        passFieldElem = driver.find_element_by_name("password1")
        confirmPassElem = driver.find_element_by_name("password2")
        submitButtonElem = driver.find_element_by_xpath("//button[contains(@type, 'submit')]")

        nameFieldelem.send_keys(self.clientuser)
        passFieldElem.send_keys(self.clientpw)
        confirmPassElem.send_keys(self.clientpw)
        ActionChains(driver).move_to_element(submitButtonElem).click(submitButtonElem).perform()
        submitButtonElem.send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.close()


# Create new spaces for proprietor users
class CreateSpaces(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  # opens a webpage

        self.index_url = "http://127.0.0.1:8000"

        # Can be changed to create new users
        self.proprietoruser = 'proprietor5'
        self.proprietorpw = 'ajkDUI3#f'

        self.sp_name = "Space space"
        self.sp_desc = "This is a space for use."

    def create_spaces(self):
        driver = self.driver

        # Redirect to login
        driver.get(self.index_url + '/create_space/')

        # Login as proprietor
        name = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        name.send_keys(self.proprietoruser)
        password.send_keys(self.proprietorpw)
        loginbutton.send_keys(Keys.RETURN)

        # Create space
        sp_name = driver.find_element_by_name("space_name")
        desc = driver.find_element_by_name("space_description")
        capacity = driver.find_element_by_name("space_max_capacity")
        noise_allowed = Select(driver.find_element_by_name("space_noise_level_allowed"))
        noise_level = Select(driver.find_element_by_name("space_noise_level"))
        wifi = driver.find_element_by_name("space_wifi")
        restroom = driver.find_element_by_name("space_restrooms")
        submitButton = driver.find_element_by_xpath("//*[contains(@type, 'submit')]")

        sp_name.send_keys(self.sp_name)
        desc.send_keys(self.sp_desc)
        capacity.send_keys(62)
        noise_allowed.select_by_index(2)
        noise_level.select_by_index(3)
        wifi.click()
        restroom.click()
        submitButton.send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.close()


# Tests @proprietor_required decorator and protected view create_space()
class ProprietorRequiredTests(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  # opens a webpage

        self.index_url = "http://127.0.0.1:8000"

        # Can be replaced with users based on your local database
        self.clientuser = 'spaceplease6'
        self.clientpw = 'jedwi5hak2'

        self.proprietoruser = 'proprietor5'
        self.proprietorpw = 'ajkDUI3#f'

    def test_client_create_space(self):
        driver = self.driver

        # Not logged in
        expected_url = self.index_url + '/login/?next=/create_space/'
        driver.get(self.index_url + '/create_space/')
        redirect_url = driver.current_url
        self.assertEqual(redirect_url, expected_url)

        # This redirected login will try to redirect to create_space
        # expecting user to be logged in as proprietor, however it will
        # not redirect as it is logging in as client
        name = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        name.send_keys(self.clientuser)
        password.send_keys(self.clientpw)
        loginbutton.send_keys(Keys.RETURN)

        # After logging in, page reloads
        self.assertEqual(self.index_url + '/login/', driver.current_url)

        # Display message when user logging in is a client
        message = driver.find_element_by_xpath("//*[contains (@class, 'messages')]")
        self.assertTrue(message)

        # Login again
        name = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        name.send_keys(self.clientuser)
        password.send_keys(self.clientpw)
        loginbutton.send_keys(Keys.RETURN)

        self.assertEqual(self.index_url + '/account/', driver.current_url)

        # Accessing create_space from client account page
        driver.get(self.index_url + '/create_space/')

        # Takes you back to login page, account is still active
        # User could potentially switch user types
        self.assertEqual(self.index_url + '/login/', driver.current_url)

    def test_proprietor_create_space(self):
        driver = self.driver

        # Not logged in
        expected_url = self.index_url + '/login/?next=/create_space/'
        driver.get(self.index_url + '/create_space/')
        redirect_url = driver.current_url
        self.assertEqual(redirect_url, expected_url)

        # Login as proprietor
        name = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        name.send_keys(self.proprietoruser)
        password.send_keys(self.proprietorpw)
        loginbutton.send_keys(Keys.RETURN)

        # Redirect to create_space page
        self.assertEqual(self.index_url + '/create_space/', driver.current_url)

    def tearDown(self):
        self.driver.close()


# Tests @user_is_space_owner decorator and protected view update_space()
# Spaces are based on id created on local database, may be different
class SpaceOwnerTests(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  # opens a webpage

        self.index_url = "http://127.0.0.1:8000"

        # Can be replaced with users based on your local database
        self.clientuser = 'spaceplease6'
        self.clientpw = 'jedwi5hak2'

        self.proprietoruser = 'proprietor5'
        self.proprietorpw = 'ajkDUI3#f'

    def test_client_access_spaces(self):
        driver = self.driver

        # Access update_space not logged in
        driver.get(self.index_url + '/update_space/1')
        self.assertEqual(self.index_url + '/update_space/1', driver.current_url)

        # Display error message
        message = driver.find_element_by_css_selector("body").text
        self.assertEqual(message, 'Permission Denied.')

        driver.get(self.index_url + '/login/')

        # Access space as a client denied
        name = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        name.send_keys(self.clientuser)
        password.send_keys(self.clientpw)
        loginbutton.send_keys(Keys.RETURN)

        driver.get(self.index_url + '/update_space/1')
        self.assertEqual(self.index_url + '/update_space/1', driver.current_url)

        # Display error message
        message = driver.find_element_by_css_selector("body").text
        self.assertEqual(message, 'Permission Denied.')

    def test_proprietor_access_spaces(self):
        driver = self.driver

        driver.get(self.index_url + '/login/')

        # Login as proprietor
        name = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_xpath("//*[contains(@class, 'btn')]")

        name.send_keys(self.proprietoruser)
        password.send_keys(self.proprietorpw)
        loginbutton.send_keys(Keys.RETURN)

        # Access own space on database
        driver.get(self.index_url + '/update_space/7')
        self.assertEqual(self.index_url + '/update_space/7', driver.current_url)

        message = driver.find_element_by_css_selector("body").text
        self.assertNotEqual(message, 'Permission Denied.')

        # Access other user's space
        driver.get(self.index_url + '/update_space/2')
        self.assertEqual(self.index_url + '/update_space/2', driver.current_url)

        # Display error message
        message = driver.find_element_by_css_selector("body").text
        self.assertEqual(message, 'Permission Denied.')

    def tearDown(self):
        self.driver.close()


# Test if the pages use the correct template
# Does not test specific details, therefore client and
# proprietor test results would be the same, since they use same template
# Only using a proprietor account is sufficient for this kind of test
class PageTemplateTests(TestCase):
    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.user)
        self.proprietor = User.objects.get(username='testuser')
        self.proprietor.is_proprietor = True
        self.assertEqual(1, User.objects.count())

        response = self.client.post('/login/', self.user, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_active)

    def test_proprietor_account_view(self):
        self.assertTrue(self.proprietor.is_proprietor)

        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)

        # Test that it is using the right templates
        self.assertTemplateUsed(response, 'sharedspaces/account.html')
        self.assertTemplateUsed(response, 'sharedspaces/account_header.html')

    def test_index_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        # Test that it is using the right templates
        self.assertTemplateUsed(response, 'sharedspaces/index.html')
        self.assertTemplateUsed(response, 'sharedspaces/account_header.html')

    def test_index_view_logged_in(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        # Test that it is using the right templates
        self.assertTemplateUsed(response, 'sharedspaces/index.html')
        self.assertTemplateUsed(response, 'sharedspaces/account_header.html')

    def test_logout_view(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

        # Test that it is using the right template
        self.assertTemplateUsed(response, 'sharedspaces/logout.html')

    def test_logo_is_on_page(self):
        response = self.client.get('')
        self.assertContains(response, 'navbar-brand')

        response = self.client.get('/account/')
        self.assertContains(response, 'navbar-brand')

        response = self.client.get('/sign_up/client/')
        self.assertContains(response, 'navbar-brand')

        response = self.client.get('/sign_up/proprietor/')
        self.assertContains(response, 'navbar-brand')

        response = self.client.get('/login/')
        self.assertContains(response, 'navbar-brand')

        response = self.client.get('/logout/')
        self.assertContains(response, 'navbar-brand')


# Added by Binh
# Tests adding tags in create_space form
class CreateSpaceTagTests(TestCase):
    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.user)
        self.proprietor = User.objects.get(username='testuser')
        self.proprietor.is_proprietor = True

    def test_form_tag_field(self):
        self.client.login(username='testuser', password='#zgsXJLY5jRb35j')
        response = self.client.get('/create_space/')
        self.assertContains(response, 'space_tags')

    def test_tags_not_required(self):
        # Taken from CreateSpaceTests
        default_data = {"space_name": 'TestName',
                        "space_description": 'Rand Description',
                        "space_max_capacity": 23,
                        "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                        "space_noise_level": [Noise_Level_Choices[1][0]],
                        "space_wifi": True,
                        "space_restrooms": False,
                        "space_food_drink": True,
                        "space_open": True}
        test_form = CreateSpaceForm(data=default_data)
        self.assertTrue(test_form.is_valid())

    def test_create_space_form_with_tags(self):
        # Taken from CreateSpaceTests
        default_data = {"space_name": 'TestName',
                        "space_description": 'Rand Description',
                        "space_max_capacity": 23,
                        "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                        "space_noise_level": [Noise_Level_Choices[1][0]],
                        "space_wifi": True,
                        "space_restrooms": False,
                        "space_food_drink": True,
                        "space_open": True,
                        "space_tags": 'lighting, spacious',
                        }
        test_form = CreateSpaceForm(data=default_data)
        self.assertTrue(test_form.is_valid())

    def test_validate_tags_create_space(self):
        # Taken from CreateSpaceTests
        default_data = {"space_name": 'TestName',
                        "space_description": 'Rand Description',
                        "space_max_capacity": 23,
                        "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                        "space_noise_level": [Noise_Level_Choices[1][0]],
                        "space_wifi": True,
                        "space_restrooms": False,
                        "space_food_drink": True,
                        "space_open": True,
                        "space_tags": 'cafe,warm',
                        }

        # submit form with tags
        self.client.login(username='testuser', password='#zgsXJLY5jRb35j')
        response = self.client.post('/create_space/', default_data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(1, Space.objects.count())

        # check if tags were added, !=0
        space = Space.objects.get(space_name=default_data['space_name'])
        self.assertNotEqual(space.space_tags.get_queryset().count(), 0)

        # check tags are correct, django-taggit has documents on parsing tags
        # but checking in case
        tag_list = space.space_tags.get_queryset()
        tag_str = 'cafe,warm'
        tag_names = tag_str.split(',')

        for i in range(tag_list.count()):
            self.assertEqual(tag_list[i].name, tag_names[i])


# Added by Binh
# Tests updating tags on update_space form, such as removing and adding tags
class UpdateSpaceTagTests(TestCase):
    # Taken from CreateSpaceTests
    TestCase.default_data = {"space_name": 'TestName',
                             "space_description": 'Rand Description',
                             "space_max_capacity": 23,
                             "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                             "space_noise_level": [Noise_Level_Choices[1][0]],
                             "space_wifi": True,
                             "space_restrooms": False,
                             "space_food_drink": True,
                             "space_open": True,
                             "space_tags": 'cafe,warm,quiet',
                             }

    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.user)
        self.proprietor = User.objects.get(username='testuser')
        self.proprietor.is_proprietor = True

        self.client.login(username='testuser', password='#zgsXJLY5jRb35j')
        response = self.client.post('/create_space/', TestCase.default_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_space_tags_appear(self):
        response = self.client.get('/update_space/1')
        self.assertEqual(response.status_code, 200)

        # make sure its the correct space page
        self.assertContains(response, 'TestName')

        # tags appear, comma separated and spaced
        # Note: tags appear in different order on front end, cannot
        # string them all in one string for assertContains
        self.assertContains(response, 'cafe')
        self.assertContains(response, 'warm')
        self.assertContains(response, 'quiet')

    def test_add_new_tag(self):
        default_data = {"space_name": 'TestName',
                        "space_description": 'Rand Description',
                        "space_max_capacity": 23,
                        "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                        "space_noise_level": [Noise_Level_Choices[1][0]],
                        "space_wifi": True,
                        "space_restrooms": False,
                        "space_food_drink": True,
                        "space_open": True,
                        "space_tags": 'cafe,warm,quiet,bright',
                        }

        # get number of tags before adding new tags
        sp = Space.objects.get(space_name=default_data['space_name'])
        tag_count = sp.space_tags.get_queryset().count()

        response = self.client.post('/update_space/1', default_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # sum of tags should be tag_count + 1 after adding new tag
        space = Space.objects.get(space_name=default_data['space_name'])
        self.assertEqual(space.space_tags.get_queryset().count(), tag_count + 1)

    def test_remove_tag(self):
        default_data = {"space_name": 'TestName',
                        "space_description": 'Rand Description',
                        "space_max_capacity": 23,
                        "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                        "space_noise_level": [Noise_Level_Choices[1][0]],
                        "space_wifi": True,
                        "space_restrooms": False,
                        "space_food_drink": True,
                        "space_open": True,
                        "space_tags": 'cafe,warm',
                        }

        # get number of tags before removing a tag
        sp = Space.objects.get(space_name=default_data['space_name'])
        old_tags = sp.space_tags.get_queryset()
        old_tag_count = old_tags.count()

        response = self.client.post('/update_space/1', default_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # sum of tags should be tag_count - 1 after removing tag
        space = Space.objects.get(space_name=default_data['space_name'])
        self.assertEqual(space.space_tags.get_queryset().count(), old_tag_count - 1)
        new_tags = space.space_tags.get_queryset()

        # compare tags
        for i in range(new_tags.count()):
            self.assertEqual(old_tags[i], new_tags[i])

    def test_remove_all_tags(self):
        default_data = {"space_name": 'TestName',
                        "space_description": 'Rand Description',
                        "space_max_capacity": 23,
                        "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                        "space_noise_level": [Noise_Level_Choices[1][0]],
                        "space_wifi": True,
                        "space_restrooms": False,
                        "space_food_drink": True,
                        "space_open": True,
                        "space_tags": '',
                        }

        # get number of tags before removing all
        sp = Space.objects.get(space_name=default_data['space_name'])
        old_tags = sp.space_tags.get_queryset().count()

        response = self.client.post('/update_space/1', default_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # should be 0
        space = Space.objects.get(space_name=default_data['space_name'])
        self.assertNotEqual(space.space_tags.get_queryset().count(), old_tags)
        self.assertEqual(space.space_tags.get_queryset().count(), 0)


# Added by Binh
# Tests for correct spaces being displayed when searching by tags
class TaggedSpacesTests(TestCase):
    # Taken from CreateSpaceTests
    TestCase.space_one = {"space_name": 'TestName',
                          "space_description": 'Rand Description',
                          "space_max_capacity": 23,
                          "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                          "space_noise_level": [Noise_Level_Choices[1][0]],
                          "space_wifi": True,
                          "space_restrooms": False,
                          "space_food_drink": True,
                          "space_open": True,
                          "space_tags": 'cafe,warm,quiet',
                          }

    TestCase.space_two = {"space_name": 'Test Space',
                          "space_description": 'Rand Description',
                          "space_max_capacity": 20,
                          "space_noise_level_allowed": [Noise_Level_Choices[2][0]],
                          "space_noise_level": [Noise_Level_Choices[1][0]],
                          "space_wifi": True,
                          "space_restrooms": False,
                          "space_food_drink": True,
                          "space_open": True,
                          "space_tags": 'cafe,popup',
                          }

    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.user)
        self.proprietor = User.objects.get(username='testuser')
        self.proprietor.is_proprietor = True

        self.client.login(username='testuser', password='#zgsXJLY5jRb35j')
        response = self.client.post('/create_space/', TestCase.space_one, follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/create_space/', TestCase.space_two, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_tagged_spaces_template(self):
        response = self.client.get('/tag/cafe')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sharedspaces/tagged_spaces.html')

    def test_tagged_spaces_listings(self):
        # 'cafe' tag should display both space listings
        response = self.client.get('/tag/cafe')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TestCase.space_one['space_name'])
        self.assertContains(response, TestCase.space_two['space_name'])

        # 'warm' tag should display only space one
        response = self.client.get('/tag/warm')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TestCase.space_one['space_name'])
        self.assertNotContains(response, TestCase.space_two['space_name'])

        # 'popup' tag should display only space two
        response = self.client.get('/tag/popup')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TestCase.space_two['space_name'])
        self.assertNotContains(response, TestCase.space_one['space_name'])
