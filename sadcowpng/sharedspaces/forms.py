from django.contrib.auth.forms import UserCreationForm

from .models import User

# Saves user as a proprietor
class ProprietorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_proprietor = True
        if commit:
            user.save()
        return user
