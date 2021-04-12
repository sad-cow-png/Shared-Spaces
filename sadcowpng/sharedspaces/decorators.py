from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Protects views only proprietors can access
# Displays message if client account tries to access protected view
def proprietor_required(function):

    def is_client(request):
        if request.user.is_client:
            messages.info(request, 'Please login as a proprietor to access page.')
            return HttpResponseRedirect(reverse('login'))

        return function(request)
    return is_client
