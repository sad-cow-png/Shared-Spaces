from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CreateSpaceForm, Noise_Level_Choices, ProprietorSignUpForm,\
    ClientSignUpForm, SpaceTimes, ReserveSpaceForm, SpaceFeedbackForm
from .models import Space, User, SpaceDateTime, SpaceFeedback
from django.db.models import Q
from itertools import chain
from .decorators import proprietor_required, user_is_space_owner, client_required, user_is_date_owner


# Shared Spaces Home Page
def index(request):
    if request.method == 'POST':
        q = request.POST.get('query')
        ufilter = request.POST.get('filters')
        # submit type lets us change the redirect
        submit_type = request.POST.get('submit_style')  # new
        space = Space.objects.filter(Q(space_name__contains=q) | Q(space_description__contains=q))
        date = SpaceDateTime.objects.filter(Q(space_date__contains=q))
        allq = chain(space, date)
        # first I check if the submit type is NOT none, meaning we want markers!
        if submit_type is not None:
            context = {
                'val': 'space',
                'space': space,
                'maps_api_key': settings.GOOGLE_MAPS_API_KEY
            }
            return render(request, 'sharedspaces/index.html', context=context)
        # The all search will comb through each model for a match case for the search query
        # Inter model searches will have chained results
        if ufilter == 'all' and submit_type is None:

            # this submit type goes to original new page, with all the fancy details
            context = {
                'val': ufilter,
                'all': allq
            }
            return render(request, 'sharedspaces/search_results.html', context=context)
        if ufilter == 'space' and submit_type is None:
            # new stuff here
            context = {
                'val': ufilter,
                'space': space
            }
            return render(request, 'sharedspaces/search_results.html', context=context)
        if ufilter == 'date' and submit_type == None:
            # new stuff here
            context = {
                'val': ufilter,
                'date': date
            }
            return render(request, 'sharedspaces/search_results.html', context=context)
    else:
        context = {
            'maps_api_key': settings.GOOGLE_MAPS_API_KEY
        }
        return render(request, 'sharedspaces/index.html', context=context)


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
            space_address1 = space_form.cleaned_data['space_address1']
            space_address2 = space_form.cleaned_data['space_address2']
            space_zip_code = space_form.cleaned_data['space_zip_code']
            space_city = space_form.cleaned_data['space_city']
            space_state = space_form.cleaned_data['space_state']
            space_country = space_form.cleaned_data['space_country']
            noise_level_allowed = int(space_form.cleaned_data["space_noise_level_allowed"][0])
            noise_level = int(space_form.cleaned_data["space_noise_level"][0])
            wifi = space_form.cleaned_data['space_wifi']
            restroom = space_form.cleaned_data['space_restrooms']
            food_drink = space_form.cleaned_data['space_food_drink']
            user = request.user
            tags = space_form.cleaned_data['space_tags']

            sp = Space(space_name=name, space_description=description, space_max_capacity=max_capacity,
                       space_address1=space_address1, space_address2=space_address2, space_zip_code=space_zip_code,
                       space_city=space_city, space_state=space_state, space_country=space_country,
                       space_noise_level_allowed=noise_level_allowed, space_noise_level=noise_level, space_wifi=wifi,
                       space_restrooms=restroom, space_food_drink=food_drink, space_owner=user, space_open=True)

            sp.save()

            primary_key = sp.pk

            # Get created space key to manually add tags
            space = Space.objects.get(pk=primary_key)
            for tag in tags:
                space.space_tags.add(tag)

            # redirecting to date and time page once complete to get at least one data and time
            # return HttpResponseRedirect(reverse('space_date_time', args=[primary_key]))
            # now redirects to the account page from which the user can add date and time to their heart's content
            return HttpResponseRedirect(reverse('account'))

    # if a GET (or any other method) we'll create a blank form
    else:
        space_form = CreateSpaceForm()

    return render(request, 'sharedspaces/create_space.html', {'form': space_form})


@login_required
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
            old_space.space_address1 = space_form.cleaned_data['space_address1']
            old_space.space_address2 = space_form.cleaned_data['space_address2']
            old_space.space_zip_code = space_form.cleaned_data['space_zip_code']
            old_space.space_city = space_form.cleaned_data['space_city']
            old_space.space_state = space_form.cleaned_data['space_state']
            old_space.space_country = space_form.cleaned_data['space_country']
            old_space.space_noise_level_allowed = int(space_form.cleaned_data["space_noise_level_allowed"][0])
            old_space.space_noise_level = int(space_form.cleaned_data["space_noise_level"][0])
            old_space.space_wifi = space_form.cleaned_data['space_wifi']
            old_space.space_restrooms = space_form.cleaned_data['space_restrooms']
            old_space.space_food_drink = space_form.cleaned_data['space_food_drink']
            old_space.space_open = space_form.cleaned_data['space_open']

            tags = space_form.cleaned_data['space_tags']

            # clear all tags
            old_space.space_tags.clear()

            # add tags, takes care of duplicates
            for tag in tags:
                if tag in old_space.space_tags.get_queryset():
                    pass
                else:
                    old_space.space_tags.add(tag)

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

        # get tags
        tag_list = old_space.space_tags.get_queryset()

        # extracting the old data into a dictionary
        old_data = {"space_name": old_space.space_name,
                    "space_description": old_space.space_description,
                    "space_max_capacity": old_space.space_max_capacity,
                    "space_address1": old_space.space_address1,
                    "space_address2": old_space.space_address2,
                    "space_zip_code": old_space.space_zip_code,
                    "space_city": old_space.space_city,
                    "space_state": old_space.space_state,
                    "space_country": old_space.space_country,
                    "space_noise_level_allowed": old_space_noise_level_allowed,
                    "space_noise_level": old_space_noise_level,
                    "space_wifi": old_space.space_wifi,
                    "space_restrooms": old_space.space_restrooms,
                    "space_food_drink": old_space.space_food_drink,
                    "space_open": old_space.space_open,
                    "space_tags": tag_list,
                    }

        # creating a form with the old data
        space_form = CreateSpaceForm(old_data)

        context = {'form': space_form, "space_id": space_id, "space": old_space,
                   "name": old_space.space_name}

    return render(request, 'sharedspaces/update_space.html', context=context)


@login_required
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


@login_required
@user_is_date_owner
def update_space_date_time(request, date_time_id):
    """
    To update the toggle for date and time
    """
    # get the space from the data base with the given space id
    old_date_time = SpaceDateTime.objects.get(pk=date_time_id)

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
                   "id": date_time_id}

    return render(request, 'sharedspaces/update_space_date_time.html', context=context)


@login_required
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
            # should not fail as date/time slots are linked on front-end
            date = form.cleaned_data['reserve_date']
            time_slot = form.cleaned_data['reserve_time_slot']

            if date.pk == time_slot.pk:
                sp_slot = SpaceDateTime.objects.get(pk=time_slot.pk)
                sp_slot.space_dt_reserved_by = request.user.username
                sp_slot.space_dt_reserved = True
                sp_slot.save()

                return HttpResponseRedirect(reverse('account'))

            else:
                form = ReserveSpaceForm(space_id=space_id)

    else:
        form = ReserveSpaceForm(space_id=space_id)

    context = {
        "form": form,
        "space": space,
        "space_id": space_id,
    }

    return render(request, 'sharedspaces/reserve_space.html', context=context)


def load_times(request):
    """
    Update available time slot based on selected date
    Gets SpaceDateTime object pk from "Available date(s)" selection box
    Filters time slot by pk for "Available time slot" box
    """
    sp_dt_id = request.GET.get('sp')
    sp_times = SpaceDateTime.objects.filter(pk=sp_dt_id)

    return render(request, 'sharedspaces/time_slot_options.html', {'sp_times': sp_times})


@login_required
@user_is_space_owner
def date_time(request, space_id):
    """
    The handles the listing of date and time for each location
    """
    if request.user.is_proprietor:
        date_times = SpaceDateTime.objects.filter(space_id=space_id)
        space = Space.objects.get(pk=space_id)

        context = {
            'date_times': date_times,
            'space': space
        }
    else:
        return HttpResponseRedirect(reverse('account'))

    return render(request, 'sharedspaces/date_time.html', context=context)


def tag_spaces(request, slug):
    """
    Filters space objects by tag and return
    to tag page based on tag slug
    """
    spaces = Space.objects.filter(space_tags__name=slug)

    context = {
        'space_list': spaces,
        'slug': slug,
    }

    return render(request, 'sharedspaces/tagged_spaces.html', context=context)


def write_feedback(request, space_id):
    # Does not restrict user feedback to logged in users - can be changed
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        space_form = SpaceFeedbackForm(request.POST)
        # check whether it's valid:
        if space_form.is_valid():
            # User writes feedback and it is saved with an association to the selected space
            # This is so when the feedback gets a page for viewing feedback it can load appropriately
            space_fb = space_form.cleaned_data['space_feedback']
            sp = SpaceFeedback(space_feedback = space_fb, space_id=Space.objects.get(pk=space_id))
            sp.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        space_form= SpaceFeedbackForm()
        context = {'form': space_form,
                   "space_id": space_id}
        return render(request, 'sharedspaces/write_feedback.html', context)
