from django.urls import path

from .views import Home, LoginUser, logout_user, \
    TaskList, CreateTask, UpdateTask, DeleteTask, \
    LabelList, CreateLabel, UpdateLabel, DeleteLabel

urlpatterns = [
    path('', Home.as_view(), name='main'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
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
