from django.test import TestCase
import unittest
from .forms import CreateSpaceForm

# Create your tests here.


# Tests will cover both newly entered form data and associated Create Spaces database
class CreateSpaceTests(TestCase):
    # Form entry accuracy tests
    def form_accuracy_name(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_name, 'TestName', 'space name submitted correctly and in accurate location')

    def form_accuracy_description(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_description, 'Rand Description', 'space description submitted correctly and in accurate location')

    def form_accuracy_capacity(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_max_capacity, 5, 'space max capacity submitted correctly and in accurate location')

    def form_accuracy_noise_allowed(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_noise_level_allowed, 1, 'space noise level allowed submitted correctly and in accurate location')

    def form_accuracy_noise_level(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_noise_level, 2, 'space noise level submitted correctly and in accurate location')

    def form_accuracy_wifi(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_wifi, True, 'space wifi availability submitted correctly and in accurate location')

    def form_accuracy_restroom(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_restrooms, False, 'space restroom availability submitted correctly and in accurate location')

    def form_accuracy_fd(self):
        # Creating a Test form with random data - data order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName', 'Rand Description', 5, 1, 2, True, False, True})
        self.assertEqual(test_form.space_food_drink, True, 'space food/drink availability submitted correctly and in accurate location')

    # Tests that cover database accuracy once form is submitted
    def form_to_database_accuracy(self):
        # Creating a Test form with random data - order follows model/form data order
        test_form = CreateSpaceForm(data={'TestName1', 'Random Description', 10, 2, 3, False, True, True})

        # Submitting test form data to the create space database
        test_form.save(using='spaces',force_insert=True)
        # Running tests to see accurate data made it's way to the database

        # Deleting this entry from the database with it's unique ID number
        test_form.delete(using='spaces')

    # Need testing to verify that database/space entries can be modified to guide next iteration
