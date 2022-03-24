# -*- coding = utf-8 -*-
from django.urls import path
from . import views

'''urlpatterns = [
    # 客户地址
    path('address/', views.address_list),
    path('user/', views.user_list)

]'''

urlpatterns = [
    url(r'^register/$', views.register, name='register'), # 用户注册
    url(r'^register_handle/$', views.register_handle, name='register_handle'), # 用户注册处理
    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'), # 退出用户登录
    url(r'^address/$', views.address, name='address'),
    url(r'^order/(?P<page>\d+)?/?$', views.order, name='order'),
    url(r'^user', views.user, name='user'), # 用户中心-信息页
]
