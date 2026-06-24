"""treeTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from api.urls import router as estimate_router  # ルーターに名前をつける

#

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('allauth.urls')),
    path('client/', include('client.urls')),
    path('fiscalyear/', include('fiscalyear.urls')),
    path('customer/', include('customer.urls')),
    path('segment/', include('segment.urls')),
    path('user/', include('user.urls')),
    path('aggregation/', include('aggregation.urls')),
    path('construction/', include('construction.urls')),
    path('estimate/', include('estimate.urls')),
    # path('api/', include('unit.urls')),  # api call
    # re_path(r'', include('unit.urls')),
    path('unit/', include('unit.urls')),
    path('api/', include('api.urls')),
    path('process/', include('process.urls')),
    path('task/', include('task.urls')),
    # path('unit_list/', RedirectView.as_view(url='/static/API_list.html')),
]
