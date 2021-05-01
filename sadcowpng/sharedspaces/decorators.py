from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Space, SpaceDateTime


# Protects views only proprietors can access
# Displays message if client account tries to access protected view
def proprietor_required(function):
    def is_not_proprietor(request):
        if not request.user.is_proprietor:
            messages.info(request, 'Please login as a proprietor to access page.')
            return HttpResponseRedirect(reverse('login'))

        return function(request)
    return is_not_proprietor


# Only the proprietor that created the space can update space
def user_is_space_owner(function):
    def is_owner(request, space_id):
        space = Space.objects.get(pk=space_id)
        if space.space_owner == request.user:
            return function(request, space_id)
        else:
            return HttpResponse('Permission Denied.')

    return is_owner


# Protects views only clients can access
# Displays message if proprietor account tries to access protected view
def client_required(function):
    def is_not_client(request, space_id):
        if not request.user.is_client:
            messages.info(request, 'Please login as a client to access page.')
            return HttpResponseRedirect(reverse('login'))
        else:
            return function(request, space_id)

    return is_not_client


# Only the proprietor that created the space can update date and time for the space
def user_is_date_owner(function):
    def is_owner(request, date_time_id):
        date = SpaceDateTime.objects.get(pk=date_time_id)
        space = date.space_id
        if space.space_owner == request.user:
            return function(request, date_time_id)
        else:
            return HttpResponse('Permission Denied.')

    return is_owner
