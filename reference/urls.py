from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from reference.views import reference_list, reference_detail, reference_list_call

app_name = 'reference'

urlpatterns = [
    path('', reference_list_call, name='reference-list'),
    path('references/', reference_list, ),
    path('references/<int:pk>/', reference_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
