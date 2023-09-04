"""
URL configuration for task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.show, name='home'),
    path('register/', views.RegView),
    # path('api/register/', views.RegView.as_view()),
    path("login/", views.login_request,name="loginname"),
    path("logout/", views.logout_request, name="logout"),
    path("upload/", views.upload, name="upload"),
    path('files/', views.file_list, name='file_list'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('update/<int:file_id>/', views.update_file, name='update_file'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    