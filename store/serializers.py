# -*- coding = utf-8 -*-
import decimal

from rest_framework import serializers
from django.db import transaction
from customers.models import Payment
from .models import Category, Goods, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'goods_count']

    goods_count = serializers.IntegerField(read_only=True)  # must have this definition


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'name', 'description', 'price', 'brand', 'inventory', 'sales', 'image_url', 'discount',
                  'category']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'goods', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'goods', 'quantity', 'total_price']

    goods = GoodsSerializer()

    def get_total_price(self, cartitem: CartItem):  # calculate total price for the cart
        return cartitem.quantity * cartitem.goods.price * cartitem.goods.discount

    total_price = serializers.SerializerMethodField(method_name='get_total_price')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['goods', 'quantity', 'order_price', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    goods = GoodsSerializer(read_only=True)

    def get_total_price(self, order_item: OrderItem):
        return order_item.quantity * order_item.order_price


class OrderSerializer(serializers.ModelSerializer):
    # def get_total_price(self, order: Order):
    #     return sum([item.quantity * item.order_price for item in order.orderitems.all()]) * order.discount

    id = serializers.IntegerField(read_only=True)
    orderitems = OrderItemSerializer(many=True, read_only=True)
    def get_total_price(self, order: Order):
        tp = 0
        for item in order.orderitems.all():
            tp += item.quantity * item.order_price
        return round(tp * decimal.Decimal(order.discount), 2)

    total_price = serializers.SerializerMethodField(method_name='get_total_price')


    class Meta:
        model = Order
        fields = ['id', 'orderitems', 'user', 'status', 'discount', 'receiver_address',
                  'payment', 'estimated_arrival_time', 'arrival_time', 'total_price']


class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_items = CartItem.objects.select_related('goods') \
                .filter(user_id=self.validated_data['user_id'])
            if len(cart_items) > 0:
                order = Order.objects.create(user_id=self.validated_data['user_id'])
                order_items = [
                    OrderItem(order=order, goods=item.goods, order_price=item.goods.price, quantity=item.quantity)
                    for item in cart_items
                ]
                OrderItem.objects.bulk_create(order_items)
                CartItem.objects.filter(user_id=self.validated_data['user_id']).delete()
            else:
                order = None
        return order