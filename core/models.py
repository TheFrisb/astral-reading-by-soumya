import uuid

from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


# Create your models here.
class InternalBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HoroscopeSign(InternalBaseModel):
    image = models.ImageField(upload_to="horoscope-signs")
    processed_png = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="PNG",
        options={"quality": 90},
    )
    processed_webp = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="WEBP",
        options={"quality": 90},
    )
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Horoscope Sign"
        verbose_name_plural = "Horoscope Signs"


class Horoscope(InternalBaseModel):
    class Frequency(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        MONTHLY = "MONTHLY", "Monthly"

    sign = models.ForeignKey(HoroscopeSign, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=7, choices=Frequency.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"{self.sign.name} - {self.frequency} Horoscope ({self.start_date} to {self.end_date})"

    class Meta:
        unique_together = ["sign", "frequency", "start_date"]
        verbose_name = "Horoscope entry"
        verbose_name_plural = "Horoscope entries"
        ordering = ["-start_date", "sign"]


class Product(InternalBaseModel):
    class Type(models.TextChoices):
        CALL_CONSULTATION = "CALL_CONSULTATION", "Call Consultation"
        WRITTEN_REPORT = "WRITTEN_REPORT", "Written Report"

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=Type.choices)
    description = models.TextField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )


class Testimonial(InternalBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="testimonials"
    )
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    content = models.TextField()

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["-created_at"]
