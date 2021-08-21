from django.urls import path

from .views import Home, LoginUser, logout_user, UserList, RegisterUser, \
    UpdateUser, DeleteUser, StatusList, CreateStatus, UpdateStatus, \
    DeleteStatus, TaskList, CreateTask, UpdateTask, DeleteTask, \
    LabelList, CreateLabel, UpdateLabel, DeleteLabel


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
    path('statuses/create/', CreateStatus.as_view(), name='create_status'),
    path('statuses/<int:pk>/update/', UpdateStatus.as_view(),
         name='update_status'),
    path('statuses/<int:pk>/delete/', DeleteStatus.as_view(),
         name='delete_status'),
    path('tasks/', TaskList.as_view(), name='task_list'),
    path('tasks/create/', CreateTask.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', UpdateTask.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', DeleteTask.as_view(), name='delete_task'),
    path('labels/', LabelList.as_view(), name='label_list'),
    path('labels/create/', CreateLabel.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', UpdateLabel.as_view(),
         name='update_label'),
    path('labels/<int:pk>/delete/', DeleteLabel.as_view(),
         name='delete_label'),
]
