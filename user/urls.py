from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from user import views

app_name = 'user'
urlpatterns = [
    path('', views.user_list_call, name='user-list'),
    path('lists/<int:client_id>/', views.user_list),
    path('detail/<int:pk>/', views.user_detail),
    path('bulk_sync/', views.bulk_sync_users, name='user-bulk-sync'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
