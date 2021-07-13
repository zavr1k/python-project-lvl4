from django.urls import path

from .views import Home, RegisterUser, LoginUser, \
    logout_user, UserList, UpdateUser, DeleteUser, StatusList, CreateStatus, \
    UpdateStatus, DeleteStatus


urlpatterns = [
    path('',  Home.as_view(), name='main'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/create/', RegisterUser.as_view(), name='register'),
    path('users/<int:pk>/update/', UpdateUser.as_view(),
         name='change_user'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(),
         name='delete_user'),
    path('statuses/', StatusList.as_view(), name='status_list'),
    path('statuses/create', CreateStatus.as_view(), name='create_status'),
    path('statuses/<int:pk>/update', UpdateStatus.as_view(),
         name='update_status'),
    path('statuses/<int:pk>/delete', DeleteStatus.as_view(),
         name='delete_status'),
]
