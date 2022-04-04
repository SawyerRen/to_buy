# -*- coding = utf-8 -*-
from rest_framework import serializers

from customers.models import Membership, User


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ["name", "password", "password2", "phone_number", "email", "gender", "membership_id"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("password not the same")
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        validated_data["membership_id"] = 1
        user = User(**validated_data)
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password"]
