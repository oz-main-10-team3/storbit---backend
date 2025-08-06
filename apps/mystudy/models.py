from django.conf import settings
from django.db import models


# 스터디 기본 정보
class Study(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_studies")
    created_at = models.DateTimeField(auto_now_add=True)
    max_members = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)


# 스터디 신청
class StudyApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    study = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)


# 스터디 참여
class StudyParticipation(models.Model):
    study = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


# 찜한 스터디
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


# 클릭 로그 (신청 현황 / 참여 클릭)
class StudyClickLog(models.Model):
    CLICK_TYPE_CHOICES = [
        ("apply_status", "Application Status View"),
        ("join_click", "Join Study Click"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    click_type = models.CharField(max_length=20, choices=CLICK_TYPE_CHOICES)
    clicked_at = models.DateTimeField(auto_now_add=True)
