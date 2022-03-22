from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Goods
from .serializers import CategorySerializer, GoodsSerializer


# Create your views here.

# 品类列表
class CategoryListView(APIView):
    def get(self, request):
        try:
            category_list = Category.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = CategorySerializer(instance=category_list, many=True)
        return Response(ser.data)


# 商品列表
class GoodsListView(APIView):
    def get(self, request):
        print(request.query_params.dict())
        category_id = request.query_params.dict().get('category_id')  # category id为0时获取全部商品，否则按品类查询
        page = request.query_params.dict().get('page')  # 页数
        page_size = request.query_params.dict().get('page_size')  # 页面大小

        if category_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        category_id = int(category_id)
        page = int(page)
        page_size = int(page_size)
        offset = (page - 1) * page_size
        try:
            if category_id != 0:
                goods_list = Goods.objects.filter(category_id=category_id)[offset:offset + page_size]
            else:
                goods_list = Goods.objects.all()[offset:offset + page_size]
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = GoodsSerializer(instance=goods_list, many=True)
        return Response(ser.data)
