from django.urls import path, re_path
# from rest_framework import routers
#
from . import views

#
# app_name = 'api'
# router = routers.DefaultRouter(trailing_slash=True)
# router.register(r'units', views.UnitViewSet)
# #
# urlpatterns = [
#     path('', views.index, name='index'),
# ]
#
# urlpatterns += router.urls
app_name = 'api'

urlpatterns = [
    #
    path('unit-options/', views.get_unit_options,),
    path('estimate-options/', views.get_estimate_options, ),

    # path('', views.ReferenceList.as_view(), name='reference_list'),  # 一覧
    # path('add/', views.ReferenceAdd.as_view(), name='reference_add'),  # 登録
    # path('edit/<int:pk>/', views.ReferenceEdit.as_view(), name='reference_edit'),  # 修正
    # path('del/<int:pk>/', views.ReferenceDel.as_view(), name='reference_del'),  # 削除
]
