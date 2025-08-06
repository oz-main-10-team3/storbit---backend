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


class StudyApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', '대기중'),
        ('approved', '승인됨'),
        ('rejected', '거절됨'),
    ]

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applicants")
    application_text = models.TextField(blank=True, null=True, help_text="자기소개 및 참여동기")
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        unique_together = ("study", "applicant") # 사용자가 한 스터디에 중복 신청 X
        verbose_name = "스터디 신청 "
        verbose_name_plural = "스터디 신청 목록"

    def __str__(self) -> str:
        return f"{self.applicant.nickname}의 {self.study.title} 신청 ({self.status})"
