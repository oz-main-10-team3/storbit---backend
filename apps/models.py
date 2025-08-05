from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)


class Study(models.Model):
    STATUS_CHOICES = [
        ("recruiting", "Recruiting"),
        ("in_progress", "In Progress"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    type = models.CharField(max_length=50)
    member = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    max_wait_member = models.IntegerField()
    schedule = models.CharField(max_length=255)
    level = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    is_live = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="led_studies")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    is_permitted = models.BooleanField(default=False)
    role = models.CharField(max_length=50)


class Event(models.Model):
    event_image = models.URLField()
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
