from datetime import timedelta, date

import lorem
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.models import Horoscope, ZodiacSigns


class Command(BaseCommand):
    help = "Generate mock monthly and yearly horoscope data for all signs for the entire year"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching horoscope signs...")
        signs = ZodiacSigns.objects.all()
        if not signs.exists():
            self.stdout.write(
                self.style.ERROR("No horoscope signs found. Please create them first.")
            )
            return

        current_year = now().year
        start_of_year = date(current_year, 1, 1)
        end_of_year = date(current_year, 12, 31)

        total_created = 0
        for sign in signs:
            # Create mock monthly horoscopes
            self.stdout.write(f"Creating monthly horoscopes for {sign.name}...")
            for month in range(1, 13):
                start_month = date(current_year, month, 1)
                end_month = (
                    date(current_year, month + 1, 1) - timedelta(days=1)
                    if month < 12
                    else end_of_year
                )
                content = (
                        f"{sign.name} Monthly Horoscope for {start_month.strftime('%B')}:\n\n"
                        + lorem.text()
                )
                obj, created = Horoscope.objects.get_or_create(
                    sign=sign,
                    frequency=Horoscope.Frequency.MONTHLY,
                    start_date=start_month,
                    end_date=end_month,
                    defaults={"content": content},
                )
                if created:
                    total_created += 1

            # Create mock yearly horoscope
            self.stdout.write(f"Creating yearly horoscope for {sign.name}...")
            content = (
                    f"{sign.name} Yearly Horoscope for {current_year}:\n\n" + lorem.text()
            )
            obj, created = Horoscope.objects.get_or_create(
                sign=sign,
                frequency=Horoscope.Frequency.YEARLY,
                start_date=start_of_year,
                end_date=end_of_year,
                defaults={"content": content},
            )
            if created:
                total_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Total horoscope entries created: {total_created}")
        )
