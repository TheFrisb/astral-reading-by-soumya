from datetime import timedelta, date

import lorem
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.models import Horoscope, HoroscopeSign


class Command(BaseCommand):
    help = "Generate mock monthly and weekly horoscope data for all signs for the entire year"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching horoscope signs...")
        signs = HoroscopeSign.objects.all()
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
            # Create mock weekly horoscopes
            self.stdout.write(f"Creating weekly horoscopes for {sign.name}...")
            weekly_date = start_of_year
            while weekly_date <= end_of_year:
                end_week = weekly_date + timedelta(days=6)
                if end_week > end_of_year:
                    end_week = end_of_year
                content = (
                    f"{sign.name} Weekly Horoscope ({weekly_date} - {end_week}):\n\n"
                    + lorem.paragraph()
                )
                obj, created = Horoscope.objects.get_or_create(
                    sign=sign,
                    frequency=Horoscope.Frequency.WEEKLY,
                    start_date=weekly_date,
                    end_date=end_week,
                    defaults={"content": content},
                )
                if created:
                    total_created += 1
                weekly_date += timedelta(days=7)

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

        self.stdout.write(
            self.style.SUCCESS(f"Total horoscope entries created: {total_created}")
        )
