from django.db import models
from django.forms import ValidationError


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
    order = models.OneToOneField(
        "core.Order",
        on_delete=models.CASCADE,
        related_name="appointment",
        null=True,
        blank=True,
    )
    is_custom_slot = models.BooleanField(default=False, verbose_name="Custom Slot")

    def clean(self):
        super().clean()
        if not self.is_custom_slot and self.order is None:
            raise ValidationError("Order must be set if 'Custom Slot' is False.")

    def __str__(self):
        if self.is_custom_slot:
            return f"Custom Slot ({self.start_time} - {self.end_time})"

        return f"{self.order} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Scheduled Appointment Slot"
        verbose_name_plural = "Scheduled Appointment Slots"
