from django.core.management.base import BaseCommand

from core.models import ZodiacSigns


class Command(BaseCommand):
    help = "Populates HoroscopeSign model with zodiac sign data from JSON."

    def handle(self, *args, **options):

        data = [
            {
                "name": "Aries",
                "symbol": "♈",
                "dateRange": "March 21 - April 19",
                "overview": "Bold and ambitious, Aries dives headfirst into challenging situations.",
                "element": "Fire",
                "ruling_planet": "Mars",
            },
            {
                "name": "Taurus",
                "symbol": "♉",
                "dateRange": "April 20 - May 20",
                "overview": "Patient and reliable, Taurus loves the security of routine.",
                "element": "Earth",
                "ruling_planet": "Venus",
            },
            {
                "name": "Gemini",
                "symbol": "♊",
                "dateRange": "May 21 - June 20",
                "overview": "Expressive and quick-witted, Gemini represents two different personalities.",
                "element": "Air",
                "ruling_planet": "Mercury",
            },
            {
                "name": "Cancer",
                "symbol": "♋",
                "dateRange": "June 21 - July 22",
                "overview": "Deeply intuitive and sentimental, Cancer can be one of the most challenging zodiac signs to get to know.",
                "element": "Water",
                "ruling_planet": "Moon",
            },
            {
                "name": "Leo",
                "symbol": "♌",
                "dateRange": "July 23 - August 22",
                "overview": "Creative and cheerful, Leo loves to bask in the spotlight.",
                "element": "Fire",
                "ruling_planet": "Sun",
            },
            {
                "name": "Virgo",
                "symbol": "♍",
                "dateRange": "August 23 - September 22",
                "overview": "Smart, sophisticated, and kind, Virgo gets the job done without complaining.",
                "element": "Earth",
                "ruling_planet": "Mercury",
            },
            {
                "name": "Libra",
                "symbol": "♎",
                "dateRange": "September 23 - October 22",
                "overview": "Peaceful and fair, Libra hates being alone.",
                "element": "Air",
                "ruling_planet": "Venus",
            },
            {
                "name": "Scorpio",
                "symbol": "♏",
                "dateRange": "October 23 - November 21",
                "overview": "Passionate and assertive, Scorpio can determine friend from foe with a single glance.",
                "element": "Water",
                "ruling_planet": "Pluto, Mars",
            },
            {
                "name": "Sagittarius",
                "symbol": "♐",
                "dateRange": "November 22 - December 21",
                "overview": "Curious and energetic, Sagittarius is one of the biggest travelers among all zodiac signs.",
                "element": "Fire",
                "ruling_planet": "Jupiter",
            },
            {
                "name": "Capricorn",
                "symbol": "♑",
                "dateRange": "December 22 - January 19",
                "overview": "Responsible and disciplined, Capricorn is the master of self-control.",
                "element": "Earth",
                "ruling_planet": "Saturn",
            },
            {
                "name": "Aquarius",
                "symbol": "♒",
                "dateRange": "January 20 - February 18",
                "overview": "Progressive and original, Aquarius pursues unique paths in life.",
                "element": "Air",
                "ruling_planet": "Uranus, Saturn",
            },
            {
                "name": "Pisces",
                "symbol": "♓",
                "dateRange": "February 19 - March 20",
                "overview": "Intuitive and artistic, Pisces can easily escape into their dream world.",
                "element": "Water",
                "ruling_planet": "Neptune, Jupiter",
            },
        ]
        for sign_data in data:
            try:
                zodiac_sign, created = ZodiacSigns.objects.update_or_create(
                    name=sign_data["name"],
                    defaults={
                        "symbol": sign_data["symbol"],
                        "element": sign_data["element"],
                        "ruling_planet": sign_data["ruling_planet"],
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created new zodiac sign: {zodiac_sign.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated zodiac sign: {zodiac_sign.name}")
                    )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Error processing zodiac sign {sign_data['name']}: {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Finished populating HoroscopeSign model.")
        )
