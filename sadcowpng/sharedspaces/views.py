from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import CreateSpaceForm, Noise_Level_Choices, ProprietorSignUpForm, ClientSignUpForm, SpaceTimes, \
    ReserveSpaceForm
from .models import Space, User, SpaceDateTime
from .decorators import proprietor_required, user_is_space_owner, client_required


# Shared Spaces Home Page
def index(request):
    return render(request, 'sharedspaces/index.html', {'maps_api_key': settings.GOOGLE_MAPS_API_KEY})


@login_required
# account page renders based on user input role
def account(request):
    if request.user.is_proprietor:
        user = request.user
        space = Space.objects.filter(space_owner=user)
        context = {
            'space': space
        }
    else:
        user = request.user
        reserved_time = SpaceDateTime.objects.filter(space_dt_reserved_by=user)

        # Find space by time slot and add to client reserved space list
        reserved_by_user = []
        for space in reserved_time:
            reservation = Space.objects.get(pk=space.space_id.pk)
            reserved_by_user.append(reservation)

        context = {
            'reserved_time': reserved_time,
            'reserved_space': reserved_by_user,
        }

    return render(request, 'sharedspaces/account.html', context=context)


# Client sign up view
def client_sign_up(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_client = True
            user.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ClientSignUpForm()
    return render(request, "sharedspaces/client_sign_up.html", {'form': form})


def sign_up(request):
    return render(request, 'sharedspaces/signup.html')


# Logs user out
def sign_out(request):
    logout(request)
    return render(request, 'sharedspaces/logout.html')


# Proprietor signup view
def proprietor_sign_up_view(request):
    if request.method == 'POST':

        form = ProprietorSignUpForm(request.POST)

        # Check if form is valid, creates user, sets user as a proprietor, and saves
        if form.is_valid():
            user = form.save(commit=False)
            user.is_proprietor = True
            user.save()

            return HttpResponseRedirect(reverse('index'))

    else:
        form = ProprietorSignUpForm()

    return render(request, 'sharedspaces/proprietor_signup.html', {'form': form})


# Client and Proprietor Login view
class UserLoginView(LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'sharedspaces/login.html'


@login_required
@proprietor_required
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
            user = request.user
            tags = space_form.cleaned_data['space_tags']

            sp = Space(space_name=name, space_description=description, space_max_capacity=max_capacity,
                       space_noise_level_allowed=noise_level_allowed, space_noise_level=noise_level, space_wifi=wifi,
                       space_restrooms=restroom, space_food_drink=food_drink, space_owner=user, space_open=True,
                       space_tags=tags)

            sp.save()

            primary_key = sp.pk

            # redirecting to date and time page once complete to get at least one data and time
            return HttpResponseRedirect(reverse('space_date_time', args=[primary_key]))

    # if a GET (or any other method) we'll create a blank form
    else:
        space_form = CreateSpaceForm()

    return render(request, 'sharedspaces/create_space.html', {'form': space_form})


@user_is_space_owner
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
            old_space.space_open = space_form.cleaned_data['space_open']
            old_space.space_tags = space_form.cleaned_data['space_tags']
            # save the updated object in the database
            old_space.save()

            # redirecting to account page once complete for now
            return HttpResponseRedirect(reverse('account'))

    # if a GET (or any other method) we'll use the data from the database to
    # create a form with the data from the database
    else:

        # getting the tuple for the multiple choice
        # the data from the multiple choice field is a string that looks l
        old_space_noise_level_allowed = Noise_Level_Choices[old_space.space_noise_level_allowed - 1]
        old_space_noise_level = Noise_Level_Choices[old_space.space_noise_level - 1]

 #       tag_list = []
  #      for tag in old_space.space_tags.tags.get_query_set():
   #         tag_list.append(tag.name)

        # extracting the old data into a dictionary
        old_data = {"space_name": old_space.space_name,
                    "space_description": old_space.space_description,
                    "space_max_capacity": old_space.space_max_capacity,
                    "space_noise_level_allowed": old_space_noise_level_allowed,
                    "space_noise_level": old_space_noise_level,
                    "space_wifi": old_space.space_wifi,
                    "space_restrooms": old_space.space_restrooms,
                    "space_food_drink": old_space.space_food_drink,
                    "space_open": old_space.space_open,
                    #"space_tags": tag_list,
                    }

        # creating a form with the old data
        space_form = CreateSpaceForm(old_data)

        context = {'form': space_form, "space_id": space_id,
                   "name": old_space.space_name}

    return render(request, 'sharedspaces/update_space.html', context=context)


@user_is_space_owner
def space_date_time(request, space_id):
    """
    Used to create the data and time for a specific space
    :param request: HTML request
    :param space_id: The pk of the space that the date and time belongs to
    :return: Redirects to account if POST else goes to the form page to fill it up
    """
    if request.method == 'POST':
        sdt = SpaceTimes(request.POST)
        if sdt.is_valid():
            space_date = sdt.cleaned_data['date']
            space_start = sdt.cleaned_data['time_start']
            space_end = sdt.cleaned_data['time_end']

            # These are default values - toggling for closing spaces and client side reservations need separate
            # implementation
            sp = SpaceDateTime(space_date=space_date,
                               space_start_time=space_start,
                               space_end_time=space_end,
                               space_dt_closed=False,
                               space_dt_reserved=False,
                               space_id=Space.objects.get(pk=space_id))
            sp.save()

            return HttpResponseRedirect(reverse('account'))
    else:
        sdt = SpaceTimes()
        context = {'form': sdt,
                   "space_id": space_id}

    return render(request, 'sharedspaces/space_date_time.html', context=context)


@user_is_space_owner
def update_space_date_time(request, data_time_id):
    """
    To update the toggle for date and time
    """
    # get the space from the data base with the given space id
    old_date_time = SpaceDateTime.objects.get(pk=data_time_id)

    if request.method == 'POST':
        sdt = SpaceTimes(request.POST)
        # to access the cleaned data
        sdt.is_valid()
        # update the object from the database with the new data
        old_date_time.space_dt_closed = sdt.cleaned_data["closed"]

        # save the updated object in the database
        old_date_time.save()

        return HttpResponseRedirect(reverse('account'))
    else:

        # extracting the old data into a dictionary
        old_data = {"date": old_date_time.space_date,
                    "time_start": old_date_time.space_start_time,
                    "time_end": old_date_time.space_end_time,
                    "closed": old_date_time.space_dt_closed}

        # setting up form to just show the closed status
        sdt = SpaceTimes(old_data)

        context = {'form': sdt,
                   "old_date_time": old_date_time,
                   "id": data_time_id}

    return render(request, 'sharedspaces/update_space_date_time.html', context=context)


@client_required
def reserve_space(request, space_id):
    """
    Clients can reserve a time on the reserve page for each listed space
    Each space page should display available times and users will be
    able to select one
    """

    space = Space.objects.get(pk=space_id)

    if request.method == 'POST':
        form = ReserveSpaceForm(request.POST, space_id=space_id)

        if form.is_valid():

            # Compared id of date and time slot to confirm date and time are correct
            reserve_space = form.cleaned_data['reservation']
            #time_slot = form.cleaned_data['reserve_time_slot']

            sp_slot = SpaceDateTime.objects.get(pk=reserve_space.pk)
            sp_slot.space_dt_reserved_by = request.user.username
            sp_slot.space_dt_reserved = True
            sp_slot.save()
            return HttpResponseRedirect(reverse('account'))

    else:
        form = ReserveSpaceForm(space_id=space_id)

    context = {
        "form": form,
        "space": space,
        "space_id": space_id,
    }

    return render(request, 'sharedspaces/reserve_space.html', context=context)

