# -*- coding = utf-8 -*-
from django.urls import path, include
from rest_framework_nested import routers

from . import views
router = routers.DefaultRouter()
router.register('address', views.AddressViewSet, basename='address')
router.register('user', views.UserViewSet, basename='user')

payments_router = routers.NestedDefaultRouter(router, 'user', lookup='user')
payments_router.register('payments', views.PaymentViewSet, basename='user-payments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(payments_router.urls))
]
