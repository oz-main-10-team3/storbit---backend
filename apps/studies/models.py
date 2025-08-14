from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.category.models import Category

User = get_user_model()


class Study(models.TextChoices):
    MASTER = "MASTER", "방장"
    MEMBER = "MEMBER", "일반 회원"


class StudyRoom(models.Model):
    STATUS_CHOICES = [
        ("recruiting", "Recruiting"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("all", "All"),
    ]

    TYPE_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("mixed", "Mixed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")  # 기본값 추가
    thumbnail_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="online")  # 기본값 추가
    is_active = models.BooleanField(default=True)
    max_wait_member = models.PositiveIntegerField(default=0)  # 기본값 추가
    schedule = models.JSONField(blank=True, null=True)
    level = models.CharField(max_length=50, default="초급")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="all")
    is_live = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="recruiting")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# 스터디 멤버
class StudyMember(models.Model):
    class Role(models.TextChoices):
        MASTER = "MASTER", "방장"
        MEMBER = "MEMBER", "일반 회원"
    class Level(models.TextChoices):
        BEGINNER = 'beginner', '왕초보'
        NOVICE = 'novice', '초보'
        INTERMEDIATE = 'intermediate', '중급'
        ADVANCED = 'advanced', '고급'
        MASTER = 'master', '마스터'
        ANY = 'any', '무관'
    level = models.CharField(max_length=10, choices=Level.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    is_permitted = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices)


# 방장 미션
class LeaderMission(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    final_goal = models.TextField()
    common_mission = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# 스터디원 미션
class DailyMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


