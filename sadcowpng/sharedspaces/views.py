from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CreateSpaceForm
from .models import Space


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


    # Need to add data fields that auto populate using authentication - will be done in models
    # This is to pull location data and account data to be able to associate them to each other within the spaces table
    # Spaces would have a "proprietor ID" field to ease having it pop up on account pages
def create_space(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        space_form = CreateSpaceForm(request.POST)
        # check whether it's valid:
        if space_form.is_valid():
            # sanitize tuple type
            name= space_form.cleaned_data['space_name']
            description= space_form.cleaned_data['space_description']
            max_capacity= space_form.cleaned_data['space_max_capacity']
            noise_level_allowed= space_form.cleaned_data.get("space_noise_level_allowed")
            noise_level= space_form.cleaned_data.get("space_noise_level")
            wifi= space_form.cleaned_data['space_wifi']
            restroom= space_form.cleaned_data['space_restrooms']
            food_drink= space_form.cleaned_data['space_food_drink']

            sp = Space(space_name=name, space_description=description, space_max_capacity=max_capacity, space_noise_level_allowed=noise_level_allowed, space_noise_level=noise_level, space_wifi=wifi, space_restrooms=restroom, space_food_drink=food_drink)
            sp.save(using='spaces')

            # redirecting to account page once complete for now
            return HttpResponseRedirect('/account/')

        # if a GET (or any other method) we'll create a blank form
    else:
        space_form = CreateSpaceForm()

    return render(request, 'sharedspaces/create_space.html',{'form': space_form})

