from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from .models import User
# Shared Spaces Home Page
def index(request):
    return render(request, 'sharedspaces/index.html')


# account page renders based on user input role
def account(request):
    return render(request, 'sharedspaces/account.html')


def login(request):
    return render(request, 'sharedspaces/login.html')


def sign_up(request):
    return render(request, 'sharedspaces/signup.html')


def create_space(request):
    return render(request, 'sharedspaces/create_space.html')

def client_sign_up(request):
    return render(request, 'sharedspaces/client_sign_up.html')
def client_signup_redirect(request):
    uname = request.POST['username']
    password = request.POST['password']
    newUser = User(username=uname, password=password, is_client=True)
    newUser.save()
    return HttpResponse('sharedspaces/index.html')