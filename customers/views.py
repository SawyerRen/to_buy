from .models import Address, User, Payment
from .serializers import AddressSerializer, UserSerializer, PaymentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPagination


# Create your views here.


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    pagination_class = DefaultPagination
    def get_queryset(self):
        return Address.objects.filter(user_id=self.kwargs['user_pk']).order_by('-id')


    def create(self, request, *args, **kwargs):
        #print(request)
        #print(request.data)
        request.data['user'] = self.kwargs['user_pk']
        if 'is_default' in request.data: # make sure there's only 1 default address
            queryset = self.get_queryset()
            if queryset.filter(is_default=1):
                q = queryset.filter(is_default=1)
                for address in q:
                    address.is_default = 0
                    address.save()
        else:
            request.data['is_default']=0

        return super().create(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = DefaultPagination

    def create(self, request, *args, **kwargs):
        if 'membership' not in request.data:
            request.data['membership'] = 1
        print(request.data)
        return super().create(request, *args, **kwargs)


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user_id=self.kwargs['user_pk'])


