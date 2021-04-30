from django.contrib import admin
from .models import User, Space, SpaceDateTime


# Register your models here.
admin.site.register(User)
admin.site.register(Space)
admin.site.register(SpaceDateTime)
