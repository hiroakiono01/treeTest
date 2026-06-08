from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from process import views

app_name = 'process'

urlpatterns = [
    path('', views.process_list_call, name='process-list'),
    path('processes/', views.process_list, ),
    path('processes/<int:pk>/', views.process_detail),
    path('bulk_sync/', views.bulk_sync_processs,),
]
urlpatterns = format_suffix_patterns(urlpatterns)
