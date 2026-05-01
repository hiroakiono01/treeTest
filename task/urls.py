from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from task import views

app_name = 'task'
urlpatterns = [
    path('', views.task_list_call, name='task-list'),
    path('tasks/', views.task_list),
    path('tasks/<int:pk>/', views.task_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
