from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from unit import views

app_name = 'unit'
urlpatterns = [
    path('', views.unit_list_call, name='unit-list'),
    path('lists/<int:client_id>/', views.unit_list),
    path('detail/<int:pk>/', views.unit_detail),
    path('bulk_sync/', views.bulk_sync_units, name='unit-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
