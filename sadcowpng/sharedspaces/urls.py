from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_up/client/', views.client_sign_up, name='client_sign_up'),
    path('create_space/', views.create_space, name='create_space'),
    path('update_space/<space_id>', views.update_space, name='update_space'),
    path('sign_up/proprietor/', views.proprietor_sign_up_view, name='proprietor_sign_up'),
    path('logout/', views.sign_out, name='logout'),
    path('space_times/<space_id>', views.space_date_time, name='space_date_time'),
    path('space_update_times/<data_time_id>', views.update_space_date_time, name='update_date_time'),
    path('reserve/<space_id>', views.reserve_space, name='reserve_space'),
    path('load_times/', views.load_times, name='load_times'),
]
