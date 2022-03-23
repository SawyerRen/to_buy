from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Address, User
from .serializers import AddressSerializer, UserSerializer


# Create your views here.
@api_view()
def address_list(request):
    queryset = Address.objects.all()
    serializer = AddressSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def user_list(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)
