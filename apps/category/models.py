from django.db import models

from apps.studies.models import Study
from config import settings


# 카테고리 모델 생성
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
