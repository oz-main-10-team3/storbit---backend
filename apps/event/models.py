from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='이벤트 제목')
    thumbnail_url = models.URLField(max_length=500, verbose_name='썸네일 이미지 URL')
    status = models.CharField(max_length=50, choices=[('진행중', '진행중'), ('종료', '종료')], verbose_name='이벤트 상태')
    start_date = models.DateTimeField(verbose_name='시작일')
    end_date = models.DateTimeField(verbose_name='종료일')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '이벤트'
        verbose_name_plural = '이벤트 목록'
        ordering = ['-created_at']