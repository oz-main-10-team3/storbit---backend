from django.contrib.auth.models import AbstractUser
from django.db import models


# 사용자 계정
class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    bio = models.TextField(blank=True)


# 스터디 플래너
class StudyPlanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="planners")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


# 쪽지함
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
