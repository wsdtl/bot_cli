"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from django.contrib.staticfiles.views import serve


def return_static(request, path, insecure=True, **kwargs) -> None:
    """静态文件路由 在没有静态文件迁移时使用"""
    
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path("", admin.site.urls),
    # re_path(r"^static/(?P<path>.*)$", return_static, name="static"),
]
