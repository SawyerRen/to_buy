from django_filters.rest_framework import FilterSet
from .models import Goods


class GoodsFilter(FilterSet):
  class Meta:
    model = Goods
    fields = {
      'category_id': ['exact'],
      'price': ['gt', 'lt']
    }