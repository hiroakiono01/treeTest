from django.urls import path, re_path
# from django.conf.urls import url, include
from django.views.generic import RedirectView

from api import views as apiViews
from estimate import views

app_name = 'estimate'
urlpatterns = [
    path('', views.EstimateList.as_view(), name='estimate_list'),  # 一覧
    path('add/', views.EstimateAdd.as_view(), name='estimate_add'),  # 登録
    path('edit/<int:pk>/', views.EstimateEdit.as_view(), name='estimate_edit'),  # 修正
    path('del/<int:pk>/', views.EstimateDel.as_view(), name='estimate_del'),  # 削除
    re_path('^estimate_tree/$', apiViews.EstimateDViewSet.as_view({'get': 'list'}), name='estimateD_list'),
]
