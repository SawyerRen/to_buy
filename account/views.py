from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import RegisterSerializer, ChangePasswordSerializer
from customers.serializers import UserSerializer

from customers.models import User


class RegisterCheckView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        phone_number = request.GET.get('phone_number')
        count = User.objects.filter(Q(email=email) | Q(phone_number=phone_number)).count()

        data = {
            'email': email,
            'phone_number': phone_number,
            'count': count
        }
        return Response(data)


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        ser = RegisterSerializer(data=data)
        # 判断密码是否相同
        ser.is_valid(raise_exception=True)
        user = ser.save()
        user_ser = UserSerializer(user)
        return Response(user_ser.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        try:
            user = User.objects.get(Q(email=email) | Q(phone_number=phone_number))
        except:
            return Response("wrong email or phone number", status=status.HTTP_404_NOT_FOUND)

        if user.password != password:
            return Response("wrong password", status=status.HTTP_400_BAD_REQUEST)

        ser = UserSerializer(instance=user)
        return Response(ser.data)


class ChangePasswordView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        old_password = request.data.get("old_password")
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response("Cannot find user", status=status.HTTP_404_NOT_FOUND)

        if user.password != old_password:
            return Response("wrong password", status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        ser = ChangePasswordSerializer(instance=user, data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
