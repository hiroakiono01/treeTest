from django.urls import path, re_path

from reference.views import ReferenceListCreateView, ReferenceDetailView, ReferenceListView

app_name = 'reference'

urlpatterns = [
    #
    path('', ReferenceListView.as_view(), name='reference-list'),
    path('references/', ReferenceListCreateView.as_view(), name='reference-add'),
    path('references/<int:pk>/', ReferenceDetailView.as_view(), name='reference-detail'),

    # path('', views.ReferenceList.as_view(), name='reference_list'),  # 一覧
    # path('add/', views.ReferenceAdd.as_view(), name='reference_add'),  # 登録
    # path('edit/<int:pk>/', views.ReferenceEdit.as_view(), name='reference_edit'),  # 修正
    # path('del/<int:pk>/', views.ReferenceDel.as_view(), name='reference_del'),  # 削除
]
