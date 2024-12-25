from datetime import time

from django.core.management.base import BaseCommand

from booking.models import WorkDay  # Adjust the import to match your app name


class Command(BaseCommand):
    help = "Create default work days (Monday to Friday, 8:00 AM to 4:00 PM)"

    def handle(self, *args, **kwargs):
        days = [
            WorkDay.Days.MONDAY,
            WorkDay.Days.TUESDAY,
            WorkDay.Days.WEDNESDAY,
            WorkDay.Days.THURSDAY,
            WorkDay.Days.FRIDAY,
        ]
        start_time = time(8, 0)  # 8:00 AM
        end_time = time(16, 0)  # 4:00 PM

        created_count = 0
        for day in days:
            workday, created = WorkDay.objects.get_or_create(
                day=day,
                defaults={
                    "start_time": start_time,
                    "end_time": end_time,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} work days created."))
        self.stdout.write(self.style.SUCCESS("Command completed successfully."))
