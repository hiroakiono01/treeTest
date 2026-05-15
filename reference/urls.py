from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from reference import views

app_name = 'reference'

urlpatterns = [
    path('', views.reference_list_call, name='reference-list'),
    path('references/', views.reference_list, ),
    path('references/<int:pk>/', views.reference_detail),
    path('bulk_sync/', views.bulk_sync_references,),
]
urlpatterns = format_suffix_patterns(urlpatterns)
