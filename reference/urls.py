from django.urls import path, re_path

from reference.views import reference_list, reference_detail, reference_list_call

app_name = 'reference'

urlpatterns = [
    #
    path('', reference_list_call, name='reference-list'),
    path('references/', reference_list,),
    path('references/<int:pk>/', reference_detail,),

    # path('', views.ReferenceList.as_view(), name='reference_list'),  # 一覧
    # path('add/', views.ReferenceAdd.as_view(), name='reference_add'),  # 登録
    # path('edit/<int:pk>/', views.ReferenceEdit.as_view(), name='reference_edit'),  # 修正
    # path('del/<int:pk>/', views.ReferenceDel.as_view(), name='reference_del'),  # 削除
]
