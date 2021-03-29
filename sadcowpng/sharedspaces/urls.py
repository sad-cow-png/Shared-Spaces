from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('login/proprietor/', views.proprietor_login_view, name='proprietor_login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_up/proprietor/', views.proprietor_sign_up_view, name='proprietor_sign_up'),
    path('create/', views.create_space, name='create_space'),

]
