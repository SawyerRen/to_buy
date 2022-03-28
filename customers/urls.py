# -*- coding = utf-8 -*-
from django.urls import path, include
from rest_framework_nested import routers

from . import views
router = routers.DefaultRouter()
router.register('user', views.UserViewSet, basename='user')

payments_router = routers.NestedDefaultRouter(router, 'user', lookup='user')
payments_router.register('payments', views.PaymentViewSet, basename='user-payments')
address_router = routers.NestedDefaultRouter(router, 'user', lookup='user')
address_router.register('address', views.AddressViewSet, basename='user-address')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(payments_router.urls)),
    path('', include(address_router.urls))
]
