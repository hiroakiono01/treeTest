from django.urls import path
from rest_framework import routers

from . import views

app_name = 'api'
router = routers.DefaultRouter(trailing_slash=True)
router.register(r'unit_info', views.UnitViewSet)
#
urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += router.urls
