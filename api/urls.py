from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'estimate_info', views.EstimateDViewSet)

urlpatterns = [
    path('', views.test_page, name='testPage'),
]

urlpatterns += router.urls
