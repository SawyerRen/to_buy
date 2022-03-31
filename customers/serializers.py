from rest_framework import serializers
from customers.models import Address, User, Payment


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'receiver_first_name', 'receiver_last_name',
                  'state', 'county', 'street', 'post_code', 'receiver_phone_number',
                  'is_default', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'email', 'gender', 'membership']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'card_number']




