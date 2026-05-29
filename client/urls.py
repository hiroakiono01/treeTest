from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from client import views

app_name = 'client'

urlpatterns = [
    path('', views.client_list_call, name='client-list'),
    path('clients/', views.client_list, ),
    path('clients/<int:pk>/', views.client_detail),
    path('bulk_sync/', views.bulk_sync_clients,),
]
urlpatterns = format_suffix_patterns(urlpatterns)