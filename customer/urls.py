from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from customer import views

app_name = 'customer'

urlpatterns = [
    path('', views.customer_list_call, name='customer-list'),
    path('lists/<int:client_id>/', views.customer_list),
    path('detail/<int:pk>/', views.customer_detail),
    path('import/', views.customer_import, name='customer-import'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
