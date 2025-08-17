from django.db import models


class Event(models.Model):
    event_image = models.ImageField(upload_to="events/", blank=True, null=True)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title
