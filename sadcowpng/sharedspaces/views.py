from django.shortcuts import render

from django.http import HttpResponse

# Shared Spaces Home Page
def index(request):
    return HttpResponse("Welcome to Shared Spaces")

# account page renders based on user input role
def account(request):
    return HttpResponse("Here is your account page!")

def login(request):
    return HttpResponse("Login here")

def sign_up(request):
    return HttpResponse("Sign up here")

def create_space(request):
    return HttpResponse("Create your space here!")
