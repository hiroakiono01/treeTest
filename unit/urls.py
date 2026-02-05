from django.urls import path

from unit import views

app_name = 'unit'

urlpatterns = [
    # user
    path('', views.UnitList.as_view(), name='unit_list'),  # 一覧
    path('add/', views.UnitAdd.as_view(), name='unit_add'),  # 登録
    path('edit/<int:pk>/', views.UnitEdit.as_view(), name='unit_edit'),  # 修正
    path('del/<int:pk>/', views.UnitDel.as_view(), name='unit_del'),  # 削除
]
