from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('create/', views.create_space, name='create_space'),
    path('client_sign_up/', views.client_sign_up, name='client_sign_up'),

]
