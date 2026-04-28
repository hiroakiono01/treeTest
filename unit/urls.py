# from django.urls import path
# from django.views.generic import RedirectView
# from unit import views
#
# app_name = 'unit'
#
# urlpatterns = [
#     # unit
#     path('', views.UnitList.as_view(), name='unit_list'),  # 一覧
#     path('add/', views.UnitAdd.as_view(), name='unit_add'),  # 登録
#     path('edit/<int:pk>/', views.UnitEdit.as_view(), name='unit_edit'),  # 修正
#     path('del/<int:pk>/', views.UnitDel.as_view(), name='unit_del'),  # 削除
# ]

from django.urls import re_path, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from api import views
from . import views

app_name = 'unit'
# router = routers.DefaultRouter(trailing_slash=True)
# router.register(r'units', views.UnitViewSet)
# #
urlpatterns = [
    # path('', views.unit_list, name='unit_list'),
    path('save_unit/', views.save_unit_api, name='save_unit'),
    path('delete_unit/<int:pk>/', views.delete_unit, name='delete_unit'),
    # re_path(r'^data/batch_save/$', views.batch_save, name="batch_save"),
    re_path(r'^$', views.unit_list, name='unit_list'),
    # re_path(r'^data/unit/(?P<pk>[0-9]+)$', views.unit_update),


    # re_path(r'^data/units/', views.UnitViewSet.as_view({'get': 'list'})),
    # re_path(r'^data/addUnit', views.unit_add),
    re_path(r'^data/(.*)$', views.data_list),



]

urlpatterns = format_suffix_patterns(urlpatterns)
