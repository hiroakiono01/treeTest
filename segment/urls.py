from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from segment import views

app_name = 'segment'
urlpatterns = [
    path('', views.segment_list_call, name='segment-list'),
    path('lists/<int:client_id>/', views.segment_list),
    path('detail/<int:pk>/', views.segment_detail),
    path('bulk_sync/', views.bulk_sync_segments, name='segment-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
