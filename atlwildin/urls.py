"""atlwildin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from tagging import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signIn),
    path('postsignIn/', views.postsignIn),
    path('logout/', views.logout, name="log"),
    path('taggerdata/', views.view_user_data, name="view_user_data"),
    path('dashboard/', views.user_dashboard, name="user_dashboard"),
    path('tagging/', views.user_tagging, name="user_tagging"),
    path('leaderboards/', views.user_leaderboards, name="user_leaderboards"),
    path('profile/', views.user_profile, name="user_profile"),
    path('userlist/', views.user_list, name="user_list"),
    path('disable/<str:id>/', views.disable_user, name='disable'),
    path('modify/', views.modify_images, name="modify_images"),
    path('quiz/', views.quiz, name="quiz"),
    path('uploading/', views.upload_interface, name="upload_interface"),
    path('upload/', views.upload_file, name="upload"),
    path('imagedata/', views.wildlife_data, name="image_data")
]
