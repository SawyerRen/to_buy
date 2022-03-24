from django.db import models
from utils.models import BaseModel
from utils.get_hash import get_hash


class UserManager(models.Manager):
    def add_user(self, username, password, email,gender):
        '''add a new user'''
        passport = self.create(username=username, password=get_hash(password), email=email,gender=gender)
        return passport

    def get_user(self, username, password):
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            passport = None
        return passport


# Create your models here.
class Membership(BaseModel):
    level = models.IntegerField()
    discount = models.DecimalField(
        max_digits=6,
        decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Membership'


class User(BaseModel):
    name = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    GENDER = [(1, 'Male'), (0, 'Female')]
    gender = models.SmallIntegerField(choices=GENDER, default=0)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    membership_expire_time = models.DateTimeField()

    objects=UserManager()
    class Meta:
        managed = False
        db_table = 'User'


class AddressManager(models.Manager):

    def get_default_address(self, user_id):
        '''user default address'''
        try:
            addr = self.get(user_id=user_id, is_default=True)
        except self.model.DoesNotExist:
            # 没有默认收货地址
            addr = None
        return addr

    def add_one_address(self, user_id, recipient_first_name, recipient_second_name, state,county,street, zip_code, recipient_phone):
        # if user has a default address
        addr = self.get_default_address(user_id=user_id)

        if addr:
            is_default = False
        else:
            is_default = True

        # add a new one
        addr = self.create(user_id=user_id,
                           recipient_first_name=recipient_first_name,
                           recipient_second_name=recipient_second_name,
                           state=state,
                           county=county,
                           street=street,
                           zip_code=zip_code,
                           recipient_phone=recipient_phone,
                           is_default=is_default)
        return addr

class Address(BaseModel):
    # user_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    objects = AddressManager()

    class Meta:
        managed = False
        db_table = 'Address'


class Payment(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Payment'
