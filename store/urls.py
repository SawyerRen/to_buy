# -*- coding = utf-8 -*-
from django.urls import path, include

from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('goods', views.GoodsViewSet, basename='goods')
router.register('front_recommend',views.frontPageGoodsVewSet,basename="front_recommend")
router.register('cartitems', views.CartItemViewSet, basename='cartitems')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('bestseller', views.BestSellerViewSet, basename='bestseller')



urlpatterns = [
    path('', include(router.urls))
]
