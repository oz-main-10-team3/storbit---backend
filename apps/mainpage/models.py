from django.db import models


class User(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    profile_image = models.URLField(blank=True, null=True)
    goal = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.title
