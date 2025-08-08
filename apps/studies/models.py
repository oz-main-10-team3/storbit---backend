from django.conf import settings
from django.db import models

from apps.category.models import Category


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
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="led_studies")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
