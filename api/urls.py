from django.urls import path

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
    path('unit-options/<int:client_id>/', views.get_unit_options,),
    path('aggr-options/<int:client_id>/', views.get_aggr_options, ),
    # path('estimate-options/', views.get_estimate_options, ),
    path('get_estimate_name/<int:client_id>/<str:estimate_no>/', views.get_estimate_name, ),
    path('get_current_client/', views.get_current_client),
    path('fiscalyear-options/<int:client_id>/', views.get_fiscalyear_options),

    path('fiscalyears/<int:client_id>/', views.get_fiscalyears, name='get_fiscalyears'),
    path('customer-options/<int:client_id>/<str:use_flg>/', views.get_customer_options),
    path('segment-options/<int:client_id>/<str:use_flg>/', views.get_segment_options),
    path('construction-options/<int:client_id>/', views.get_construction_options),
    path('user-options/<int:client_id>/<str:use_flg>/', views.get_user_options),
    # path('', views.ReferenceList.as_view(), name='reference_list'),  # 一覧
    # path('add/', views.ReferenceAdd.as_view(), name='reference_add'),  # 登録
    # path('edit/<int:pk>/', views.ReferenceEdit.as_view(), name='reference_edit'),  # 修正
    # path('del/<int:pk>/', views.ReferenceDel.as_view(), name='reference_del'),  # 削除
]
