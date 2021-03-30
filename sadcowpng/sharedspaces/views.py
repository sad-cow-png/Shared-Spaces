from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .models import User
from .forms import ProprietorSignUpForm, ClientSignUpForm

# Shared Spaces Home Page


def index(request):
    return render(request, 'sharedspaces/index.html')

# account page renders based on user input role


def account(request):
    return render(request, 'sharedspaces/account.html')


def login(request):
    return render(request, 'sharedspaces/login.html')

# Proprietor sign up view


class ProprietorSignUpView(CreateView):
    model = User
    form_class = ProprietorSignUpForm
    template_name = 'sharedspaces/proprietor.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'proprietor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.save()
        return HttpResponseRedirect('index.html')


class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'sharedspaces/client_sign_up.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.save()
        return HttpResponseRedirect('index.html')


# Proprietor login view
#class ProprietorLoginView(CreateView):
    # client
    # proprietor
def sign_up(request):
    return render(request, 'sharedspaces/signup.html')


def create_space(request):
    return render(request, 'sharedspaces/create_space.html')


