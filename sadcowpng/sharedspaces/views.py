from django.shortcuts import render

from django.http import HttpResponse
#Shared Spaces Home Page
def index(request):
    return HttpResponse("Welcome to Shared Spaces")

def account(request):
    return HttpResponse("Here is your account page!")

def login(request):
    return HttpResponse("Login here")

def signup(request):
    return HttpResponse("Sign up here")

def createspace(request):
    return HttpResponse("Create your space here!")
