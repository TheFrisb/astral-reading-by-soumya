import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from solo.models import SingletonModel


# Create your models here.
class InternalBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ZodiacSigns(InternalBaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    element = models.CharField(max_length=20)
    ruling_planet = models.CharField(max_length=20)
    image = models.ImageField(
        null=True,
        upload_to="zodiac_signs/",
        help_text="Image representing the zodiac sign.",
    )

    sortable_order = models.IntegerField(default=0, db_index=True)

    def get_absolute_url(self):
        return reverse("core:horoscope_detail", kwargs={"sign_name": self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Zodiac Sign"
        verbose_name_plural = "Zodiac Signs"
        ordering = ["sortable_order"]


class Horoscope(InternalBaseModel):
    class Frequency(models.TextChoices):
        MONTHLY = "MONTHLY", "Monthly"
        YEARLY = "YEARLY", "Yearly"

    sign = models.ForeignKey(
        ZodiacSigns, on_delete=models.CASCADE, related_name="horoscopes"
    )
    frequency = models.CharField(max_length=7, choices=Frequency.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    content = CKEditor5Field("Content")

    @property
    def get_display_name(self):
        return f"{self.sign.name} - {self.get_frequency_display()} Horoscope"

    @property
    def get_preview(self):
        plain_text = strip_tags(self.content)  # Remove HTML tags
        words = plain_text.split()[:20]  # Get the first 20 words
        return " ".join(words)

    def __str__(self):
        return f"{self.sign.name} - {self.get_frequency_display()} Horoscope ({self.start_date} to {self.end_date})"

    class Meta:
        unique_together = ["sign", "frequency", "start_date"]
        verbose_name = "Horoscope entry"
        verbose_name_plural = "Horoscope entries"
        ordering = ["-start_date", "sign"]

        indexes = [
            models.Index(fields=["sign", "frequency", "start_date", "end_date"]),
        ]


class Reading(InternalBaseModel):
    """
    Represents a general reading service (e.g., Mini Reading, Natal Chart).
    """

    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="readings/")
    optimized_image = ImageSpecField(
        source="image",
        processors=[SmartResize(400, 225)],
        format="JPEG",
        options={"quality": 80},
    )
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

    class CallDuration(models.IntegerChoices):
        FIFTEEN = 15, "15 minutes"
        THIRTY = 30, "30 minutes"
        FORTY_FIVE = 45, "45 minutes"
        SIXTY = 60, "60 minutes"
        SEVENTY_FIVE = 75, "75 minutes"
        NINETY = 90, "90 minutes"

    reading = models.ForeignKey(
        "Reading",
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
    call_duration = models.PositiveIntegerField(
        choices=CallDuration.choices,
        blank=True,
        null=True,
        help_text="Applicable only for Call Consultations: duration of the call in minutes.",
    )

    @property
    def get_display_name(self):
        return f"{self.reading.name} {self.get_type_display()}"

    @property
    def sale_price(self):
        if self.is_discounted and self.discounted_price:
            return self.discounted_price
        return self.regular_price

    def clean(self):
        if self.type == self.Type.CALL and not self.call_duration:
            raise ValidationError(
                "Call length must be specified for Call Consultation types."
            )
        if self.type == self.Type.REPORT and self.call_duration:
            raise ValidationError(
                "Call length is not applicable for Written Report types."
            )

    def __str__(self):
        call_info = (
            f" ({self.get_call_duration_display()})"
            if self.type == self.Type.CALL and self.call_duration
            else ""
        )
        return f"{self.reading.name} {self.get_type_display()}{call_info} - ${self.regular_price}"

    class Meta:
        verbose_name = "Reading Type"
        verbose_name_plural = "Reading Types"
        ordering = ["reading__name", "type"]
        unique_together = [
            "reading",
            "type",
        ]


class Testimonial(InternalBaseModel):
    order_item = models.OneToOneField(
        "OrderItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonial",
        help_text="The order item this testimonial is for.",
    )
    reading_type = models.ForeignKey(
        ReadingType,
        on_delete=models.CASCADE,
        related_name="testimonials",
        help_text="The reading type this testimonial is for.",
    )
    full_name = models.CharField(max_length=100, blank=True, null=True)

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField()
    is_active = models.BooleanField(default=False, db_index=True)

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


class Order(InternalBaseModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    def get_purchased_reading_type(self):
        return self.item.reading_type

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id}"


class OrderInformation(InternalBaseModel):
    class DayPart(models.TextChoices):
        AM = "AM", "AM"
        PM = "PM", "PM"

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="information"
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    birth_country = models.CharField(max_length=100)
    birth_state = models.CharField(max_length=100)
    birth_city = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    time_of_birth = models.CharField(max_length=255)
    day_part = models.CharField(max_length=2, choices=DayPart.choices)
    comment = models.TextField(blank=True)

    @property
    def place_of_birth(self):
        return f"{self.birth_city}, {self.birth_state}, {self.birth_country}"

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = "Order Information"
        verbose_name_plural = "Order Information"


class OrderItem(InternalBaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="item")
    reading_type = models.ForeignKey(
        ReadingType, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.reading_type.reading.name} {self.reading_type.get_type_display()} - ${self.get_total_price()}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-created_at"]


class SiteSettings(SingletonModel):
    thank_you_template_id = models.CharField(max_length=255, blank=True)
    leave_a_review_template_id = models.CharField(max_length=255, blank=True)
    hero_title = models.CharField(max_length=255, verbose_name="Hero Title")
    hero_subtitle = models.TextField(verbose_name="Hero Subtitle")
    hero_background_image = models.ImageField(
        upload_to="hero/", verbose_name="Hero Background Image"
    )

    show_video_section = models.BooleanField(default=False)
    video_section_header = models.CharField(max_length=255, blank=True)
    video_section_header_subtitle = models.TextField(blank=True)
    video_section_video = models.FileField(upload_to="videos/", blank=True)
    video_section_video_thumbnail = models.ImageField(
        upload_to="videos/", blank=True, verbose_name="Video Thumbnail"
    )
    video_section_description_header = models.CharField(max_length=255, blank=True)
    video_section_description_header_subtitle = models.TextField(blank=True)

    def get_hero_section_details(self):
        return {
            "title": self.hero_title,
            "subtitle": self.hero_subtitle,
            "background_image_url": self.hero_background_image.url,
        }

    def get_video_section_details(self):
        return {
            "show_video_section": self.show_video_section,
            "video_section_header": self.video_section_header,
            "video_section_header_subtitle": self.video_section_header_subtitle,
            "video_section_video_url": (
                self.video_section_video.url if self.video_section_video else ""
            ),
            "video_section_video_thumbnail_url": (
                self.video_section_video_thumbnail.url
                if self.video_section_video_thumbnail
                else ""
            ),
            "video_section_description_header": self.video_section_description_header,
            "video_section_description_header_subtitle": self.video_section_description_header_subtitle,
        }

    def __str__(self):
        return "Site Settings"


class Location(InternalBaseModel):
    country_code = models.CharField(
        max_length=2, verbose_name="Country Code"
    )  # ISO country code
    postal_code = models.CharField(
        max_length=20, verbose_name="Postal Code"
    )  # Not used directly but kept for data reference
    town = models.CharField(max_length=180, verbose_name="Town")  # Place name
    state_name = models.CharField(
        max_length=100, verbose_name="State Name"
    )  # Admin name1
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    full_address = models.TextField(db_index=True)

    def __str__(self):
        return f"{self.town}, {self.state_name}, {self.country_code}"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        indexes = [
            models.Index(fields=["town"]),
            models.Index(fields=["country_code", "state_name", "town"]),
        ]


class AboutUsSettings(SingletonModel):
    personal_picture = models.ImageField(
        upload_to="about_us/",
        verbose_name="Personal Picture",
        help_text="Image representing the person or team behind the service.",
    )

    section_1_header = models.CharField(max_length=255)
    section_1_description = models.TextField()
    section_2_header = models.CharField(max_length=255)
    section_2_description = models.TextField()
    inspirational_quote = models.TextField()
    section_3_header = models.CharField(max_length=255)
    section_3_description = models.TextField()
    email = models.EmailField()
    instagram = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    @property
    def cleaned_phone_number(self):
        # return phone number without whitespace, '-', '+', and parantheses
        return

    def __str__(self):
        return "About Us Settings"


class AboutUsSection(InternalBaseModel):
    title = models.CharField(max_length=255)
    sortable_order = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.title


class AboutUsSectionCard(InternalBaseModel):
    section = models.ForeignKey(AboutUsSection, on_delete=models.CASCADE, related_name="cards")
    image = models.ImageField(upload_to="about_us/", verbose_name="Image")
    title = models.CharField(max_length=255)
    description = models.TextField()
    sortable_order = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.title