import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


# Create your models here.
class InternalBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HoroscopeSign(InternalBaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse("core:horoscope_detail", kwargs={"sign_name": self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Horoscope Sign"
        verbose_name_plural = "Horoscope Signs"
        ordering = ["name"]


class Horoscope(InternalBaseModel):
    class Frequency(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        MONTHLY = "MONTHLY", "Monthly"

    sign = models.ForeignKey(
        HoroscopeSign, on_delete=models.CASCADE, related_name="horoscopes"
    )
    frequency = models.CharField(max_length=7, choices=Frequency.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()

    @property
    def get_display_name(self):
        return f"{self.sign.name} - {self.get_frequency_display()} Horoscope"

    def __str__(self):
        return f"{self.sign.name} - {self.get_frequency_display()} Horoscope ({self.start_date} to {self.end_date})"

    class Meta:
        unique_together = ["sign", "frequency", "start_date"]
        verbose_name = "Horoscope entry"
        verbose_name_plural = "Horoscope entries"
        ordering = ["-start_date", "sign"]


class Reading(InternalBaseModel):
    """
    Represents a general reading service (e.g., Mini Reading, Natal Chart).
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)
    sortable_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Reading"
        verbose_name_plural = "Readings"
        ordering = ["name"]  # Orders readings alphabetically


class ReadingType(InternalBaseModel):
    """
    Represents a specific type of reading service (e.g., Call Consultation, Written Report).
    """

    class Type(models.TextChoices):
        CALL = "CALL", "Call Consultation"
        REPORT = "REPORT", "Written Report"

    reading = models.ForeignKey(
        Reading,
        on_delete=models.CASCADE,
        related_name="variants",
        help_text="The general reading service this type belongs to.",
    )
    type = models.CharField(
        max_length=6,
        choices=Type.choices,
        help_text="The type of this reading (e.g., Call or Report).",
    )
    regular_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="The standard price of this reading type.",
    )
    discounted_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional discounted price of this reading type.",
    )

    is_discounted = models.BooleanField(
        default=False,
        help_text="Whether this reading type is currently discounted.",
    )

    def __str__(self):
        return f"{self.reading.name} {self.get_type_display()} - ${self.regular_price}"

    class Meta:
        verbose_name = "Reading Type"
        verbose_name_plural = "Reading Types"
        ordering = ["reading__name", "type"]
        unique_together = [
            "reading",
            "type",
        ]  # Ensures each reading can have only one Call/Report type


class Testimonial(InternalBaseModel):
    reading = models.ForeignKey(
        Reading, on_delete=models.CASCADE, related_name="testimonials"
    )
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    content = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["-created_at"]


class FrequentlyAskedQuestion(InternalBaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    sortable_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "Frequently Asked Questions"
        ordering = ["sortable_order", "question"]
