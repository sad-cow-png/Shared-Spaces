from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('create_space/', views.create_space, name='create-space'),
    path('update_space/<space_id>', views.update_space, name='update-space'),


]
