# -*- coding = utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    # 查询邮箱或手机号是否已经注册过
    path('register_check', views.RegisterCheckView.as_view()),
    # 注册
    path('register', views.RegisterView.as_view()),
    # 登录
    path('login', views.LoginView.as_view()),
    # 修改密码
    path('change_password', views.ChangePasswordView.as_view()),

]
