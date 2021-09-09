from django.urls import path

from .views import Home, LoginUser, logout_user,\
    StatusList, CreateStatus, UpdateStatus, \
    DeleteStatus, TaskList, CreateTask, UpdateTask, DeleteTask, \
    LabelList, CreateLabel, UpdateLabel, DeleteLabel


urlpatterns = [
    path('',  Home.as_view(), name='main'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
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
