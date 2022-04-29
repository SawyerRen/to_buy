from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from customers.models import Address, User, Payment

# Create your models here.
from utils.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'

    def __str__(self):
        return self.name


class Goods(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods')
    brand = models.CharField(max_length=255)
    inventory = models.IntegerField()
    sales = models.IntegerField()
    image_url = models.CharField(max_length=255, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=0, default=1)

    class Meta:
        managed = False
        db_table = 'Goods'


class CartItem(BaseModel):
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitems')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='cartitems')


    class Meta:
        unique_together = [['user', 'goods']]  # make sure that a cart has unique product
        managed = False
        db_table = 'Cartitem'


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', null=True)
    status = models.SmallIntegerField(default=0)
    discount = models.FloatField(default=1)
    receiver_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders',null=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True)
    estimated_arrival_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'Order'


class OrderItem(models.Model):
    quantity = models.IntegerField()
    goods = models.ForeignKey(Goods, on_delete=models.PROTECT, related_name='orderitems')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    order_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Orderitem'