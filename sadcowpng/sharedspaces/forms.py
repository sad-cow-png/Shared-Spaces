
from django.contrib.auth.forms import UserCreationForm; from .models import User
























# Used for proprietor sign up view
class ProprietorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
