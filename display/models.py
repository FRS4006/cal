from django.db import models
from django.utils import timezone

class CalendarEvent(models.Model):
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    date_of_event = models.DateTimeField(default=timezone.now)
    zoom_url = models.URLField(blank=True)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null= True)


    def __str__(self):
        return f"{self.title}"

# Create your models here.
