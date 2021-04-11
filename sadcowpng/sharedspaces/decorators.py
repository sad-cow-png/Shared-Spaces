from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test, login_required


# Protects views only proprietors can access
def proprietor_required(function, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login/'):
    def is_proprietor(u):
        if login_required and u.is_authenticated and u.is_proprietor:
            return True

    actual_decorator = user_passes_test(
        is_proprietor,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

