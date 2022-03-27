# -*- coding = utf-8 -*-
from rest_framework import serializers
from .models import Category, Goods, Cart, CartItem


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


class CartItemSerializer(serializers.ModelSerializer): # get method for Cart details
    goods = GoodsSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'goods', 'quantity', 'total_price']

    def get_total_price(self, cartitem: CartItem): # calculate total price for the cart
        return cartitem.quantity * cartitem.goods.price

    total_price = serializers.SerializerMethodField(method_name='get_total_price')


class UpdateCartItemSerializer(serializers.ModelSerializer): # serializer for updating the cart
    class Meta:
        model = CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):
    goods_id = serializers.IntegerField() # because product_id is dynamically generated at run time, so we need to specify here so that it will show up in the post form.

    class Meta:
        model = CartItem
        fields = ['id', 'goods_id', 'quantity']

    def validate_product_id(self, value): # define custom validate methods, notice the naming convention
        if not Goods.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given goods_id')
        return value

    def save(self, **kwargs): # define custom save method
        cart_id = self.context['cart_id'] # this cart_id is from the nested url, should be sent as context from views
        goods_id = self.validated_data['goods_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, goods_id=goods_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart: Cart):
        return sum(item.quantity * item.goods.price for item in cart.items.all())

    def get_items(self, cart: Cart):
        queryset = CartItem.objects.filter(cart_id=cart.id)
        serializer = CartItemSerializer(queryset, many=True)
        return serializer.data

    items = serializers.SerializerMethodField(method_name='get_items')
