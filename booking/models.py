from django.db import models


# Create your models here.
class WorkDay(models.Model):
    class Days(models.TextChoices):
        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"
        SATURDAY = "Saturday"
        SUNDAY = "Sunday"

    day = models.CharField(max_length=10, choices=Days, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Work Day"
        verbose_name_plural = "Work Days"


class ScheduledAppointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    order = models.OneToOneField("core.Order", on_delete=models.CASCADE, related_name="appointment")

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    class Meta:
        verbose_name = "Appointment Slot"
        verbose_name_plural = "Appointment Slots"