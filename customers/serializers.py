from rest_framework import serializers
from customers.models import Address, User, Payment

# free delivery state
sql = '''select distinct A.*, number
from (select state, count(*) as number
      from Address
      group by state) as sub
         join Address A on A.state = sub.state
         join User U on A.user_id = U.id
where number >= 15
order by number desc;'''
queryset = Address.objects.raw(sql)
hashtable = set()
for i in queryset:
    if len(hashtable) >= 15:
        break
    hashtable.add(i.state)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'receiver_first_name', 'receiver_last_name',
                  'state', 'county', 'street', 'post_code', 'receiver_phone_number',
                  'is_default', 'user', 'free_delivery']

    def delivery_state(self, address: Address):
        #print(address.state)
        return address.state in hashtable


    free_delivery = serializers.SerializerMethodField(method_name='delivery_state')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'email', 'gender', 'membership']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'card_number']
