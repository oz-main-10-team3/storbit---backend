from django.db import models


class Event(models.Model):
    class EventType(models.TextChoices):
        REWARD = "reward_event", "리워드 이벤트"
        IZAKAYA = "izakaya_event", "이자카야 이벤트"
        POPULAR_IZAKAYA = "popular_izakaya_event", "인기이자카야 이벤트"
        SEASON = "season_limited", "시즌한정판"

    class EventStatus(models.TextChoices):
        ONGOING = "ongoing", "진행중"
        FINISHED = "finished", "종료"
        ON_HOLD = "on_hold", "보류중"
        SCHEDULED = "scheduled", "예정"

    event_type = models.CharField(choices=EventType.choices, max_length=30)
    event_status = models.CharField(choices=EventStatus.choices, max_length=20)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_image")
    event_image = models.ImageField(upload_to="events/", blank=True, null=True)
