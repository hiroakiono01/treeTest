from django.urls import path

from estimate import views

app_name = 'estimate'

urlpatterns = [
    # estimate
    path('', views.EstimateList.as_view(), name='estimate_list'),  # 一覧
    path('add/', views.EstimateAdd.as_view(), name='estimate_add'),  # 登録
    path('edit/<int:pk>/', views.EstimateEdit.as_view(), name='estimate_edit'),  # 修正
    path('del/<int:pk>/', views.EstimateDel.as_view(), name='estimate_del'),  # 削除
    path('testPage/', views.test_page, name='testPage'),
    path('estimate_tree/', views.estimate_tree, name='estimate_tree'),
]
