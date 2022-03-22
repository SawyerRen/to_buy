from django.db import models

# Create your models here.
from utils.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'


class Goods(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    inventory = models.IntegerField()
    sales = models.IntegerField()
    image_url = models.CharField(max_length=255, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=0, default=1)

    class Meta:
        managed = False
        db_table = 'Goods'
