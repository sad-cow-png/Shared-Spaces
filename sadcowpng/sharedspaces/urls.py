from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # account page renders based on user input role
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.createspace, name='createspace'),

]