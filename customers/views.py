from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .models import Address, User
from .serializers import AddressSerializer, UserSerializer


# Create your views here.

class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressList(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer