from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Space


# Protects views only proprietors can access
# Displays message if client account tries to access protected view
def proprietor_required(function):
    def is_client(request):
        if request.user.is_client:
            messages.info(request, 'Please login as a proprietor to access page.')
            return HttpResponseRedirect(reverse('login'))

        return function(request)
    return is_client


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
    def is_proprietor(request, space_id):
        if request.user.is_proprietor:
            messages.info(request, 'Please login as a client to access page.')
            return HttpResponseRedirect(reverse('login'))
        else:
            return function(request, space_id)

    return is_proprietor
