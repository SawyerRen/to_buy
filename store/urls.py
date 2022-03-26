# -*- coding = utf-8 -*-
from django.urls import path, include

from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('goods', views.GoodsViewSet, basename='goods')
router.register('carts', views.CartViewSet)

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('cartitems', views.CartItemViewSet, basename='cart-cartitems')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(carts_router.urls))
]
