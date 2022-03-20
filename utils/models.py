# -*- coding = utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    """为模型类补充字段"""
    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True
