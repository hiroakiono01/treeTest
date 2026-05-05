from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from task import views

app_name = 'task'
urlpatterns = [
    path('', views.task_list_call, name='task_list'),
    path('', views.task_tree_test_call, name='task_tree_test'),
    path('tasks_test/', views.tree_list_test),
    # path('tasks/<int:pk>/', views.tree_detail),
    path('lists/<int:estimate_no>/', views.task_list),
    path('detail/<int:pk>/', views.task_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
