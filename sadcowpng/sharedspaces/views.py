from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CreateSpaceForm, Noise_Level_Choices
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
    """
    used to create the spaces. Only accessed by the proprietors (need to add this requirement).
    :param request: rhe html request passed when accessing the page
    :return: either the account page when the request is post so the data for creating a new
    space is stored else the create space page where the user can enter a new space
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        space_form = CreateSpaceForm(request.POST)
        # check whether it's valid:
        if space_form.is_valid():
            # sanitize tuple type
            name = space_form.cleaned_data['space_name']
            description = space_form.cleaned_data['space_description']
            max_capacity = space_form.cleaned_data['space_max_capacity']
            noise_level_allowed = int(space_form.cleaned_data["space_noise_level_allowed"][0])
            noise_level = int(space_form.cleaned_data["space_noise_level"][0])
            wifi = space_form.cleaned_data['space_wifi']
            restroom = space_form.cleaned_data['space_restrooms']
            food_drink = space_form.cleaned_data['space_food_drink']

            sp = Space(space_name=name, space_description=description, space_max_capacity=max_capacity,
                       space_noise_level_allowed=noise_level_allowed, space_noise_level=noise_level, space_wifi=wifi,
                       space_restrooms=restroom, space_food_drink=food_drink)
            sp.save()

            # redirecting to account page once complete for now
            return HttpResponseRedirect('/account/')

    # if a GET (or any other method) we'll create a blank form
    else:
        space_form = CreateSpaceForm()

    return render(request, 'sharedspaces/create_space.html', {'form': space_form})


def update_space(request, space_id):
    """
    Renders the page for updating the spaces stored in the database
    Need to implement the restriction to only allow proprietors edit the spaces.
    :param space_id: Represents the id with which the space is stored in the database
    :param request: The html request passed when accessing the page
    :return: either the account page when the request is post so the data for creating a new
    space is stored else the create space page where the user can enter a new space
    """

    # get the space from the data base with the given space id
    old_space = Space.objects.get(pk=space_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        space_form = CreateSpaceForm(request.POST)
        # check whether it's valid:
        if space_form.is_valid():
            # update the object from the database with the new data
            old_space.space_name = space_form.cleaned_data['space_name']
            old_space.space_description = space_form.cleaned_data['space_description']
            old_space.space_max_capacity = space_form.cleaned_data['space_max_capacity']
            old_space.space_noise_level_allowed = int(space_form.cleaned_data["space_noise_level_allowed"][0])
            old_space.space_noise_level = int(space_form.cleaned_data["space_noise_level"][0])
            old_space.space_wifi = space_form.cleaned_data['space_wifi']
            old_space.space_restrooms = space_form.cleaned_data['space_restrooms']
            old_space.space_food_drink = space_form.cleaned_data['space_food_drink']

            # save the updated object in the database
            old_space.save()

            # redirecting to account page once complete for now
            return HttpResponseRedirect('/account/')

    # if a GET (or any other method) we'll use the data from the database to
    # create a form with the data from the database
    else:

        # getting the tuple for the multiple choice
        # the data from the multiple choice field is a string that looks l
        old_space_noise_level_allowed = Noise_Level_Choices[old_space.space_noise_level_allowed - 1]
        old_space_noise_level = Noise_Level_Choices[old_space.space_noise_level - 1]

        # extracting the old data into a dictionary
        old_data = {"space_name": old_space.space_name,
                    "space_description": old_space.space_description,
                    "space_max_capacity": old_space.space_max_capacity,
                    "space_noise_level_allowed": old_space_noise_level_allowed,
                    "space_noise_level": old_space_noise_level,
                    "space_wifi": old_space.space_wifi,
                    "space_restrooms": old_space.space_restrooms,
                    "space_food_drink": old_space.space_food_drink}

        # creating a form with the old data
        space_form = CreateSpaceForm(old_data)

    return render(request, 'sharedspaces/update_space.html', {'form': space_form, "space_id": space_id})
