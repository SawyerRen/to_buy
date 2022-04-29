import http.client

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
from .models import Category, Goods, CartItem, Order, OrderItem
from .serializers import CategorySerializer, GoodsSerializer, CartItemSerializer, AddCartItemSerializer, \
    OrderSerializer, OrderItemSerializer, CreateOrderSerializer
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


class BestSellerViewSet(ModelViewSet):
    serializer_class = GoodsSerializer
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        category_id = self.request.query_params.dict().get('category_id')
        if category_id is None:
            return Goods.objects.filter(sales__gt=1800)
        category_id = int(category_id)
        sql = "CALL GetGoods({})".format(category_id)
        q = Goods.objects.raw(sql)
        return q


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price','sales']
    filterset_class = GoodsFilter

    def destroy(self, request, pk):
        goods = get_object_or_404(Goods, pk=pk)
        print(goods.orderitems.count())
        if goods.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        goods.delete()
        return Response(status.HTTP_204_NO_CONTENT)


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
        q = CartItem.objects.filter(user__id=user_id)
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)

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


class frontPageGoodsVewSet(ModelViewSet):
    sql_str = """ select G.*
    from Goods G left join (select max(sales) as best_good_sale, count(*) as number, brand
                            from Goods
                            where sales >=300
                            group by brand) as sub1 using (brand)
    where G.price<=10.00 and sub1.number>=5 and sales=best_good_sale
    order by G.sales desc
    limit 15"""
    queryset = Goods.objects.raw(sql_str)

    serializer_class = GoodsSerializer


    def destroy(self, request, pk):
        goods = get_object_or_404(Goods, pk=pk)
        print(goods.orderitems.count())
        if goods.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        goods.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class OrderViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        uid = self.request.query_params.dict().get('user_id')
        if uid is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, headers={'No user_id': 'user_id must be provided'})
        q = Order.objects.filter(user__id=uid)
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


