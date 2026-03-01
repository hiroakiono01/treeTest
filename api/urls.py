from django.urls import path
from rest_framework import routers

from . import views

app_name = 'api'
router = routers.DefaultRouter(trailing_slash=True)
router.register(r'estimateD_info', views.EstimateDViewSet, basename='estimateD_info')
router.register(r'unit_info', views.UnitViewSet)
# router.register(r'estimateD_retrieve', views.EstimateDDetail, basename='estimateD_retrieve')
#
urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += router.urls
