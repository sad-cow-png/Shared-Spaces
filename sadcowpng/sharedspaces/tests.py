from django.test import TestCase
from selenium import webdriver
import unittest

# Create your tests here.

#client sign up test!

class clientSignUp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox() #opens a webpage
        # create some good and bad info for the accounts
        self.goodUname = "AnnakinSkywalker101"
        self.goodPW = "thisIsAGoodPassword1#@"
        self.goodUname2 = "JobiKenobi"
        self.badPw = "pass1"

    def goodSignUpTest(self):
        driver = self.driver
        driver.get("127.0.0.1:8000/sign_up/client")