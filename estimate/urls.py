from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from estimate import views

app_name = 'estimate'

urlpatterns = [
    path('', views.estimate_list_call, name='estimate-list'),  # 一覧
    path('lists/<int:client_id>/<str:sql>/', views.estimate_list),  # 登録
    # path('add/<int:client_id>/', views.estimate_add),  # 登録
    path('detail/<int:pk>/', views.estimate_detail),  # 修正
]
urlpatterns = format_suffix_patterns(urlpatterns)
