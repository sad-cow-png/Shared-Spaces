from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

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


def client_sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uname = form.cleaned_data.get('username')
            raw_pw = form.cleaned_data.get('password1')
            user = authenticate(username=uname, password=raw_pw)
            login(request , user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, "sharedspaces/client_sign_up.html", {'form': form})

'''
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
'''
# Proprietor login view
#class ProprietorLoginView(CreateView):
    # client
    # proprietor
def sign_up(request):
    return render(request, 'sharedspaces/signup.html')


def create_space(request):
    return render(request, 'sharedspaces/create_space.html')


