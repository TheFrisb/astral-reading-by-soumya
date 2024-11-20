from django.core.management.base import BaseCommand

from core.models import HoroscopeSign


class Command(BaseCommand):
    help = "Create all 12 horoscope signs"

    def handle(self, *args, **kwargs):
        horoscope_signs = [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]

        created_count = 0
        for sign in horoscope_signs:
            obj, created = HoroscopeSign.objects.get_or_create(name=sign)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created horoscope sign: {sign}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Horoscope sign already exists: {sign}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Total horoscope signs created: {created_count}")
        )
