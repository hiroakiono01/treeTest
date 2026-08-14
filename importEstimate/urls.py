from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from importEstimate import views

app_name = 'importEstimate'

urlpatterns = [
    path('', views.import_estimate.as_view(), name='import-estimate'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
