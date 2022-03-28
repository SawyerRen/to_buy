from django.db.models import Count
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Goods, CartItem
from .serializers import CategorySerializer, GoodsSerializer, CartItemSerializer, AddCartItemSerializer
from store.pagination import DefaultPagination
from .filters import GoodsFilter


# Create your views here.

# 品类列表
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(goods_count=Count('goods')).all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination

    def destroy(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        c = category.goods.count()
        print(c)
        if c > 0:
            return Response({'error': 'Category cannot be deleted because it includes one or more products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price']
    filterset_class = GoodsFilter

    def destroy(self, request, pk):
        goods = get_object_or_404(Goods, pk=pk)
        print(goods.orderitems.count())
        if goods.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        goods.delete()
        return Response(status.HTTP_204_NO_CONTENT)


# class CartViewSet(CreateModelMixin,
#                   RetrieveModelMixin,
#                   DestroyModelMixin,
#                   GenericViewSet):  # because we don't need to support other functions yet
#     serializer_class = CartSerializer
#     queryset = Cart.objects.prefetch_related('items__goods').all()
#
#     def create(self, request, *args, **kwargs):
#         user_id = request.data.get('user', None)
#         q = self.get_queryset()
#         if len(q.filter(user_id=user_id)) == 1:
#             instance = q.get(user_id=user_id)
#             serializer = self.get_serializer(instance)
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Cart Found': 'Cart with the user_id already exists'})
#         return super().create(request, *args, **kwargs)
#
#
# class CartItemViewSet(ModelViewSet):
#     http_method_names = ['get', 'post', 'patch', 'delete']
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return AddCartItemSerializer
#         elif self.request.method == 'PATCH':
#             return UpdateCartItemSerializer
#         return CartItemSerializer
#
#     def get_serializer_context(self):
#         return {'cart_id': self.kwargs['cart_pk']}
#
#     def get_queryset(self):
#         return CartItem.objects.filter(cart_id=self.kwargs['user_pk']).select_related('goods')

#get, post, put, patch, delete
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        user_id = self.request.query_params.dict().get('user_id')
        return CartItem.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.dict().get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, headers={'No user_id':'user_id must be provided'})
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        goods_id = self.request.data['goods']
        user_id = self.request.data['user']
        try:
            cartitem = CartItem.objects.get(goods_id=goods_id, user_id=user_id)
            cartitem.quantity += self.request.data['quantity']
            cartitem.save()
            serializer = self.get_serializer(cartitem)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return super().create(request, *args, **kwargs)






