from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from fiscalyear import views

app_name = 'fiscalyear'
urlpatterns = [
    path('', views.fiscalyear_list_call, name='fiscalyear-list'),
    path('lists/<int:client_id>/', views.fiscalyear_list),
    path('detail/<int:pk>/', views.fiscalyear_detail),
    path('bulk_sync/', views.bulk_sync_fiscalyears, name='fiscalyear-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
