from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'estimateD_read', views.EstimateDViewSet, 'estimate_tree')
router.register(r'estimateD_create', views.EstimateDCreateViewSet, 'estimate_tree_create')

router.register(r'unit_info', views.UnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('estimate_tree/<str:estimate_no>/', views.EstimateDViewSet.as_view({"get": 'list'}), name='estimate_tree_view'),
]



