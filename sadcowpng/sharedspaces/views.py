from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from .models import User
from .forms import ProprietorSignUpForm


# Shared Spaces Home Page
def index(request):
    return render(request, 'sharedspaces/index.html')


# account page renders based on user input role
@login_required
def account(request):
    return render(request, 'sharedspaces/account.html')


def login(request):
    return render(request, 'sharedspaces/login.html')


# Proprietor login view
class ProprietorLoginView(LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'sharedspaces/proprietor_login.html'


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

        # Check if form is valid, saves user, and sets user as a proprietor
        if form.is_valid():
            user = form.save(commit=False)
            user.is_proprietor = True
            user.save()

            return HttpResponseRedirect(reverse('index'))

    else:
        form = ProprietorSignUpForm()

    return render(request, 'sharedspaces/proprietor_signup.html', {'form': form})


def create_space(request):
    return render(request, 'sharedspaces/create_space.html')
