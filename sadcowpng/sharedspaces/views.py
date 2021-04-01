from django.shortcuts import render, redirect, reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .models import User
from .forms import ClientSignUpForm


# Shared Spaces Home Page
def index(request):
    return render(request, 'sharedspaces/index.html')


# account page renders based on user input role
def account(request):
    return render(request, 'sharedspaces/account.html')


def login(request):
    return render(request, 'sharedspaces/login.html')


# Proprietor sign up view
def client_sign_up(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_client = True
            user.save()
            return HttpResponseRedirect(reverse('/'))
    else:
        form = ClientSignUpForm()
    return render(request, "sharedspaces/client_sign_up.html", {'form': form})


def sign_up(request):
    return render(request, 'sharedspaces/signup.html')


def create_space(request):
    return render(request, 'sharedspaces/create_space.html')
