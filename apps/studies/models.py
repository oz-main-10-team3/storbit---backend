from django.conf import settings
from django.db import models

from apps.category.models import Category
from apps.users.models import User


class Study(models.Model):
    STATUS_CHOICES = [
        ("recruiting", "Recruiting"),
        ("in_progress", "In Progress"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("all", "All"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=100)
    member = models.IntegerField()
    is_active = models.BooleanField(default=True)
    max_wait_member = models.IntegerField()
    schedule = models.CharField(max_length=255)
    level = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    is_live = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="led_studies")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.title


# 스터디 멤버
class StudyMember(models.Model):
    class Role(models.TextChoices):
        MASTER = "MASTER", "방장"
        MEMBER = "MEMBER", "일반 회원"

    class Level(models.TextChoices):
        BEGINNER = "beginner", "왕초보"
        NOVICE = "novice", "초보"
        INTERMEDIATE = "intermediate", "중급"
        ADVANCED = "advanced", "고급"
        MASTER = "master", "마스터"
        ANY = "any", "무관"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Level.choices)
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
