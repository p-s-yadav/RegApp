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
from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.RegAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('upload/', views.UploadAPIView.as_view()),
    path('update/<int:file_id>', views.UpdateFileAPIView.as_view()),
    path('download/<int:file_id>', views.DownloadAPIView.as_view()),
    path('delete/<int:file_id>', views.DeleteFileAPIView.as_view()),
    path('upload_csv/', views.CSVUploadAPIView.as_view()),

]
    