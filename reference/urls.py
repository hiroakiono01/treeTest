from django.urls import path

from reference import views

app_name = 'reference'

urlpatterns = [
    # user
    path('', views.ReferenceList.as_view(), name='reference_list'),  # 一覧
    path('add/', views.ReferenceAdd.as_view(), name='reference_add'),  # 登録
    path('edit/<int:pk>/', views.ReferenceEdit.as_view(), name='reference_edit'),  # 修正
    path('del/<int:pk>/', views.ReferenceDel.as_view(), name='reference_del'),  # 削除
]
