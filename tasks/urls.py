from django.urls import path

from .views import Home, \
    TaskList, CreateTask, UpdateTask, DeleteTask


urlpatterns = [
    path('', Home.as_view(), name='main'),
    path('tasks/', TaskList.as_view(), name='task_list'),
    path('tasks/create/', CreateTask.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', UpdateTask.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', DeleteTask.as_view(), name='delete_task'),
]
