"""resource URL Configuration

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
from . import views
from admin_view import views as admin_view
from user_view import views as user_view
from material import views as material_view

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',user_view.profile,name='profile'),
    path('logout/',views.userLogout,name='logout'),
    path('register/',views.userRegister,name='register'),
    path('login/',views.userLogin,name='login'),
    path('upload_material/',material_view.upload_material,name='upload_material'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='reset_password.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name="password_reset_complete"),
    path('issue/',user_view.issue,name='issue'),
    path('issuestatus/',user_view.issuestatus,name='issuestatus'),
    path('reportedcontent/',user_view.reportedcontent,name='reportedcontent'),
    path('notifications/',user_view.notifications,name='notifications'),
    path('removenotification/<int:id>/',user_view.removenotification,name='removenotification'),
    path('youruploads/',user_view.youruploads,name='youruploads'),
    path('searching/',user_view.searching,name='searching'),
    path('explore/<int:id>/',views.explore,name='explore'),
    path('adminissue',admin_view.adminissue,name='adminissue'),
    path('adminflag',admin_view.adminflag,name='adminflag'),
    path('issue_status/<int:id>/<str:act>/', admin_view.address_issues, name="issue_status"),
    path('issue_delete/<int:id>/', user_view.issue_delete, name="issue_delete"),
    path('admin_delete/<int:id>/', admin_view.issue_delete, name="admin_delete"),
    path('like/<int:id>/',user_view.like,name='like'),
    path('dislike/<int:id>/',user_view.dislike,name='dislike'),
    path('report/<int:id>/',user_view.report,name='report'),
    path('filter/',user_view.filter,name='filter'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)