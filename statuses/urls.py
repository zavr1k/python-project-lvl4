from django.urls import path

from .views import CreateStatus
from .views import DeleteStatus
from .views import StatusList
from .views import UpdateStatus


urlpatterns = [
    path('',
         StatusList.as_view(),
         name='status_list'),

    path('create/',
         CreateStatus.as_view(),
         name='create_status'),

    path('<int:pk>/update/',
         UpdateStatus.as_view(),
         name='update_status'),

    path('<int:pk>/delete/',
         DeleteStatus.as_view(),
         name='delete_status'),
    ]
