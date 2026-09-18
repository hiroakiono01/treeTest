from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from aggregation import views

app_name = 'aggregation'
urlpatterns = [
    path('', views.aggregation_list_call, name='aggregation-list'),
    path('lists/<int:client_id>/', views.aggregation_list),
    path('detail/<int:pk>/', views.aggregation_detail),
    path('bulk_sync/', views.bulk_sync_aggregations, name='aggregation-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
