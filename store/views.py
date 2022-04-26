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
from .models import Category, Goods, CartItem, Order, OrderItem, GoodsTable
from .serializers import CategorySerializer, GoodsSerializer, CartItemSerializer, AddCartItemSerializer, \
    OrderSerializer, OrderItemSerializer, CreateOrderSerializer, GoodsTableSerializer
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


name_map = {'name':'name', 'description':'description',
            'price':'price', 'category_id' :'category_id', 'brand':'brand',
            'inventory' :'inventory', 'sales':'sales', 'image_url':'image_url',
            'discount':'discount','is_deleted':'is_deleted', 'created_at':'created_at','updated_at':'updated_at'
            }


class GoodsTableViewSet(ModelViewSet):
    sql = """
    CALL GetGoods()
    """
    queryset = GoodsTable.objects.raw(sql)
    serializer_class = GoodsTableSerializer


class GoodsViewSet(ModelViewSet):
    sql = """
    CALL GetGoods()
    """
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
        user_id = self.request.query_params.dict().get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, headers={'No user_id': 'user_id must be provided'})
        return super().list(request, *args, **kwargs)

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


