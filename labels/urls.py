from django.urls import path

from .views import CreateLabel
from .views import DeleteLabel
from .views import LabelList
from .views import UpdateLabel

urlpatterns = [
    path('',
         LabelList.as_view(),
         name='label_list'),
    path('create/',
         CreateLabel.as_view(),
         name='create_label'),
    path('<int:pk>/update/',
         UpdateLabel.as_view(),
         name='update_label'),
    path('<int:pk>/delete/',
         DeleteLabel.as_view(),
         name='delete_label'),
]