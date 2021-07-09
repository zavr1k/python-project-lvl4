from django.urls import path
from .views import Home, RegisterUser, LoginUser, logout_user, UserList, UpdateUser, DeleteUser

urlpatterns = [
    path('',  Home.as_view(), name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/create/', RegisterUser.as_view(), name='register'),
    path('users/<int:pk>/update/', UpdateUser.as_view(), name='change_user'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='delete_user'),
]
