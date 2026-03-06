from django.urls import path, re_path

from api import views as apiViews
from estimate import views

# from django.conf.urls import url, include

app_name = 'estimate'
urlpatterns = [
    path('', views.EstimateList.as_view(), name='estimate_list'),  # 一覧
    path('add/', views.EstimateAdd.as_view(), name='estimate_add'),  # 登録
    path('edit/<int:pk>/', views.EstimateEdit.as_view(), name='estimate_edit'),  # 修正
    path('del/<int:pk>/', views.EstimateDel.as_view(), name='estimate_del'),  # 削除
    re_path('^estimate_tree/$', apiViews.EstimateDViewSet.as_view({'get': 'list', 'post': "create"}), name='estimateD_list'),
    re_path('^estimate_tree/$<int:id>/', apiViews.EstimateDViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name='estimateD_detail'),
]
