from django.test import TestCase
from django.urls import reverse

from .models import User
from .forms import ClientSignUpForm


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
        response = self.client.get('/sign_up/client/') # move to client sign up page
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
                'data' : {
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
        user = User.objects.get(username= 'JobiBenKenobi')
        self.assertEqual(user.is_client, True)
        # we may also want to check the user has is_prop false
        self.assertEqual(user.is_proprietor, False)
        self.assertRedirects(response, 'index')

