"""
@ author: neo
@ date: 2023-12-15  11:02 
@ file_name: urls.PY
@ github: https://github.com/Underson888/
"""
from django.urls import path
from django.urls import re_path

from . import views
from .forms import LoginForm
# 这里定义的app的名字
app_name = "account"

urlpatterns = [re_path(r'^login/$',
                       views.LoginView.as_view(success_url='/'),
                       name='login',
                       kwargs={'authentication_form': LoginForm}),
               re_path(r'^register/$',
                       views.RegisterView.as_view(success_url="/"),
                       name='register'),
               re_path(r'^logout/$',
                       views.LogoutView.as_view(),
                       name='logout'),
               path(r'BJSTAccount/result.html',
                    views.account_result,
                    name='result'),
               re_path(r'^forget_password/$',
                       views.ForgetPasswordView.as_view(),
                       name='forget_password'),
               re_path(r'^forget_password_code/$',
                       views.ForgetPasswordEmailCode.as_view(),
                       name='forget_password_code'),
               ]