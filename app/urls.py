from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

]
