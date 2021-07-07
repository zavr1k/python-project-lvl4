from django.urls import path
from .views import Home, RegisterUser, LoginUser, logout_user

urlpatterns = [
    path('',  Home.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
