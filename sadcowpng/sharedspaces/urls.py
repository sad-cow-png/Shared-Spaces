from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_up/client/', views.client_sign_up, name='client_sign_up'),
    path('create/', views.create_space, name='create_space'),
    path('create_space/', views.create_space, name='create_space'),
    path('update_space/<space_id>', views.update_space, name='update_space'),
    path('sign_up/proprietor/', views.proprietor_sign_up_view, name='proprietor_sign_up'),
    path('logout/', views.sign_out, name='logout'),
]
