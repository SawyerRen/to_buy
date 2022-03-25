from .models import Address, User, Payment
from .serializers import AddressSerializer, UserSerializer, PaymentSerializer
from rest_framework.viewsets import ModelViewSet
from .pagination import DefaultPagination


# Create your views here.


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    pagination_class = DefaultPagination


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

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.kwargs['user_pk']
        return super().create(request, *args, **kwargs)


