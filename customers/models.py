from django.db import models
from utils.models import BaseModel


# Create your models here.
class Address(BaseModel):
    user_id = models.IntegerField()
    receiver_first_name = models.CharField(max_length=255)
    receiver_last_name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    post_code = models.CharField(max_length=64)
    receiver_phone_number = models.CharField(max_length=64)
    IS_DEFAULT = [(1, 'Yes'), (0, 'No')]
    is_default = models.SmallIntegerField(choices=IS_DEFAULT,
                                          default=0)

    class Meta:
        managed = False
        db_table = 'Address'


class User(BaseModel):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    GENDER = [(1, 'Male'), (0, 'Female')]
    gender = models.SmallIntegerField(choices=GENDER, default=0)
    membership_level = models.IntegerField()
    membership_expire_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'User'


class Membership(BaseModel):
    level = models.IntegerField()
    discount = models.models.DecimalField(
        max_digits=6,
        decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.models.models.DecimalField(
        max_digits=6,
        decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Membership'


class Payment(BaseModel):
    user_id = models.IntegerField()
    card_number = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Payment'
