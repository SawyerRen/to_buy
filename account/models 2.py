from django.db import models
from utils.models import BaseModel
from customers.models import   Membership, User


# # Create your models here.
# class Membership(BaseModel):
#     level = models.IntegerField(unique=True)
#     discount = models.DecimalField(max_digits=10, decimal_places=0)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     class Meta:
#         managed = False
#         db_table = 'Membership'
#
#
# class User(BaseModel):
#     name = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     gender = models.IntegerField(blank=True, null=True)
#     membership = models.ForeignKey(Membership, models.DO_NOTHING)
#     membership_expire_time = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'User'
