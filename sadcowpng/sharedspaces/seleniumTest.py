from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# Create your tests here.

#client sign up test!

class clientSignUp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome() #opens a webpage
        # create some good and bad info for the accounts
        self.goodUname = "AnnakinSkywalker101"
        self.goodPW = "thisIsAGoodPassword1#@"
        self.goodUname2 = "JobiKenobi"
        self.badPw = "pass1"

    def test_goodSignUpTest(self):
        driver = self.driver
        driver.get("127.0.0.1:8000/sign_up/client")
        self.assertIn("Client Sign Up", driver.title)
        # get the fields for each
        nameFieldelem = driver.find_element_by_name("username")
        passFieldElem = driver.find_element_by_name("password1")
        confirmPassElem = driver.find_element_by_name("password2")
        submitButtonElem = driver.find_element_by_xpath("/html/body/form/button")
        # try a good one
        nameFieldelem.send_keys(self.goodUname)
        passFieldElem.send_keys(self.goodPW)
        confirmPassElem.send_keys(self.goodPW)
        submitButtonElem.send_keys(Keys.RETURN)
        # this should be a good uname and password, so we can check if we get to the index

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
