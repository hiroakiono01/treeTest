from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from task import views

app_name = 'task'
urlpatterns = [
    path('', views.task_list_call, name='task_list'),
    path('task_tree_test/', views.task_tree_test, name='task_tree_test'),
    # path('tasks_test/', views.tree_list_test),
    # path('tasks/<int:pk>/', views.tree_detail),
    path('lists/<int:estimateId>/', views.task_list),
    path('detail/<int:pk>/', views.task_detail),
    path('bulk_sync/', views.bulk_sync_tasks, name='task-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
