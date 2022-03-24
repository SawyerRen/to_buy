# -*- coding = utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    # 客户地址
    path('address/', views.AddressList.as_view()),
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),
    path('address/<int:pk>', views.AddressDetail.as_view())
]
