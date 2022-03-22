# -*- coding = utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    # 品类列表
    path('categories/', views.CategoryListView.as_view()),
    # 商品列表
    path('goods/', views.GoodsListView.as_view()),
]
