from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from construction import views

app_name = 'construction'
urlpatterns = [
    path('', views.construction_list_call, name='construction-list'),
    path('lists/<int:client_id>/', views.construction_list),
    path('detail/<int:pk>/', views.construction_detail),
    path('bulk_sync/', views.bulk_sync_constructions, name='construction-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
