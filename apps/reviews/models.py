from django.db import models

from apps.studies.models import Study
from apps.users.models import User


class Review(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
