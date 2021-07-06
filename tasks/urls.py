from django.urls import path
from .views import Home, RegisterUser


urlpatterns = [
    path('',  Home.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register')
]
