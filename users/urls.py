from django.urls import path

from .views import UserList
from .views import RegisterUser
from .views import UpdateUser
from .views import DeleteUser

urlpatterns = [
    path('', UserList.as_view(), name='users'),
    path('create/', RegisterUser.as_view(), name='register'),
    path('<int:pk>/update/', UpdateUser.as_view(),
         name='change_user'),
    path('<int:pk>/delete/', DeleteUser.as_view(),
         name='delete_user')
    ]
