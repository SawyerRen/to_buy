# -*- coding = utf-8 -*-
from rest_framework import serializers

from customers.models import Payment
from .models import Category, Goods, CartItem


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


