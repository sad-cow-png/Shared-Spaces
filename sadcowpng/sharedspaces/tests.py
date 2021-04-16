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
                    'username': 'test',
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

        response = self.client.post('sign_up/client_sign_up', data=good_data)
        self.assertEqual(response.status_code, 302)
        # right now, we should have 2 more objects from start
        self.assertEqual(User.objects.count(), self.precount + 2)

        # find that user and check if he/she has is_client
        user = User.objects.get(username='JobiBenKenobi')
        self.assertEqual(user.is_client, True)
        # we may also want to check the user has is_prop false
        self.assertEqual(user.is_proprietor, False)
        self.assertRedirects(response, 'index')


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


# Test proprietor login form and view
class ProprietorLoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': '#zgsXJLY5jRb35j',
        }
        User.objects.create_user(**self.credentials)
        user = User.objects.all()
        self.assertTrue(user.count(), 1)

    def test_login_view(self):
        response = self.client.get('/login/proprietor/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='sharedspaces/proprietor_login.html')

    def test_login_fields(self):
        response = self.client.get('/login/proprietor/')
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

    def test_login(self):
        response = self.client.post('/login/proprietor/', self.credentials, follow=True)
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

