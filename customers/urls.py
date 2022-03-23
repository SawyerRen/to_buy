# -*- coding = utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    # 客户地址
    path('address/', views.address_list),
    path('user/', views.user_list)

]
