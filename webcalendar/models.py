from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Calendar(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="calendars")
    sharedUsers = models.ManyToManyField("User", related_name="sharedUsers", blank=True)
    title = models.CharField(max_length=100)
    def Calendar_Attributes(self):
        return {"title": self.title, "id": self.id}
    
class Event(models.Model):
    startHour = models.IntegerField()
    startMin = models.IntegerField()
    endMin = models.IntegerField()
    endHour = models.IntegerField()
    day = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255) 
    calendar = models.ForeignKey("Calendar", on_delete=models.CASCADE, related_name="events")
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="created_events")
    def Event_Attributes(self):
        return {"day": self.day,
                "title": self.title,
                "cal":self.calendar.Calendar_Attributes()}
    