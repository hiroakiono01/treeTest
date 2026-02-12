from django.urls import path

from detailMaster import views

app_name = 'detailMaster'

urlpatterns = [
    # user
    path('', views.DetailMasterList.as_view(), name='detailMaster_list'),  # 一覧
    path('add/', views.DetailMasterAdd.as_view(), name='detailMaster_add'),  # 登録
    path('edit/<int:pk>/', views.DetailMasterEdit.as_view(), name='detailMaster_edit'),  # 修正
    path('del/<int:pk>/', views.UDetailMasterDel.as_view(), name='detailMaster_del'),  # 削除
]
