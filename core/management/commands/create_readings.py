import random

from django.core.management.base import BaseCommand

from core.models import Reading, ReadingType, Testimonial


class Command(BaseCommand):
    help = "Create readings with call and written types, and 5 testimonials per reading"

    # Mini Reading Options
    MINI_READING_OPTIONS = [
        "Health",
        "Career",
        "Love Life",
        "Wealth",
        "Marriage",
        "Children",
        "Past Life Karma",
    ]

    READING_TEMPLATES = [
        {
            "name": "Mini Reading",
            "description": "A short reading focusing on specific areas.",
        },
        {
            "name": "In-depth Natal Chart Reading",
            "description": "Comprehensive analysis of your natal chart.",
        },
        {
            "name": "Child’s Profile Reading",
            "description": "Detailed astrological profile for a child.",
        },
    ]

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating readings and testimonials...")

        for reading_data in self.READING_TEMPLATES:
            # Create the Reading
            reading, created = Reading.objects.get_or_create(
                name=reading_data["name"],
                defaults={
                    "description": reading_data["description"],
                    "is_active": True,
                },
            )
            if created:
                self.stdout.write(f"Created Reading: {reading.name}")
            else:
                self.stdout.write(f"Reading already exists: {reading.name}")

            # Create Call and Report types for the Reading
            for reading_type in [ReadingType.Type.CALL, ReadingType.Type.REPORT]:
                ReadingType.objects.get_or_create(
                    reading=reading,
                    type=reading_type,
                    defaults={
                        "regular_price": round(random.uniform(50, 200), 2),
                        "discounted_price": (
                            round(random.uniform(30, 100), 2)
                            if random.choice([True, False])
                            else None
                        ),
                        "is_discounted": random.choice([True, False]),
                    },
                )
                self.stdout.write(f"  Added {reading_type} type for {reading.name}")

            # Create 5 Testimonials for each Reading
            for i in range(5):
                Testimonial.objects.create(
                    reading=reading,
                    name=f"Testimonial User {i + 1}",
                    rating=random.randint(3, 5),
                    content=f"This is a testimonial for {reading.name}. Amazing service!",
                    is_active=True,
                )
                self.stdout.write(f"  Created Testimonial {i + 1} for {reading.name}")

        self.stdout.write("Completed creating readings and testimonials.")
