import requests
from django.core.files.base import ContentFile
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
                "image": "https://media-public.canva.com/fwOXE/MAEqYkfwOXE/1/t.png",
            },
            {
                "name": "Taurus",
                "symbol": "♉",
                "dateRange": "April 20 - May 20",
                "overview": "Patient and reliable, Taurus loves the security of routine.",
                "element": "Earth",
                "ruling_planet": "Venus",
                "image": "https://media-public.canva.com/ELrrc/MAEqYuELrrc/1/t.png",
            },
            {
                "name": "Gemini",
                "symbol": "♊",
                "dateRange": "May 21 - June 20",
                "overview": "Expressive and quick-witted, Gemini represents two different personalities.",
                "element": "Air",
                "ruling_planet": "Mercury",
                "image": "https://media-public.canva.com/W_MPM/MAEqYkW_MPM/1/t.png",
            },
            {
                "name": "Cancer",
                "symbol": "♋",
                "dateRange": "June 21 - July 22",
                "overview": "Deeply intuitive and sentimental, Cancer can be one of the most challenging zodiac signs to get to know.",
                "element": "Water",
                "ruling_planet": "Moon",
                "image": "https://media-public.canva.com/Zo52M/MAEqYpZo52M/1/t.png",
            },
            {
                "name": "Leo",
                "symbol": "♌",
                "dateRange": "July 23 - August 22",
                "overview": "Creative and cheerful, Leo loves to bask in the spotlight.",
                "element": "Fire",
                "ruling_planet": "Sun",
                "image": "https://media-public.canva.com/H1I9c/MAEqYhH1I9c/1/t.png",
            },
            {
                "name": "Virgo",
                "symbol": "♍",
                "dateRange": "August 23 - September 22",
                "overview": "Smart, sophisticated, and kind, Virgo gets the job done without complaining.",
                "element": "Earth",
                "ruling_planet": "Mercury",
                "image": "https://media-public.canva.com/n4klY/MAEqYkn4klY/1/t.png",
            },
            {
                "name": "Libra",
                "symbol": "♎",
                "dateRange": "September 23 - October 22",
                "overview": "Peaceful and fair, Libra hates being alone.",
                "element": "Air",
                "ruling_planet": "Venus",
                "image": "https://media-public.canva.com/Wa_EE/MAEqYlWa_EE/1/t.png",
            },
            {
                "name": "Scorpio",
                "symbol": "♏",
                "dateRange": "October 23 - November 21",
                "overview": "Passionate and assertive, Scorpio can determine friend from foe with a single glance.",
                "element": "Water",
                "ruling_planet": "Pluto, Mars",
                "image": "https://media-public.canva.com/54TeI/MAEqYk54TeI/1/t.png",
            },
            {
                "name": "Sagittarius",
                "symbol": "♐",
                "dateRange": "November 22 - December 21",
                "overview": "Curious and energetic, Sagittarius is one of the biggest travelers among all zodiac signs.",
                "element": "Fire",
                "ruling_planet": "Jupiter",
                "image": "https://media-public.canva.com/-H1oA/MAEqYo-H1oA/1/t.png",
            },
            {
                "name": "Capricorn",
                "symbol": "♑",
                "dateRange": "December 22 - January 19",
                "overview": "Responsible and disciplined, Capricorn is the master of self-control.",
                "element": "Earth",
                "ruling_planet": "Saturn",
                "image": "https://media-public.canva.com/qB2zw/MAEqYiqB2zw/1/t.png",
            },
            {
                "name": "Aquarius",
                "symbol": "♒",
                "dateRange": "January 20 - February 18",
                "overview": "Progressive and original, Aquarius pursues unique paths in life.",
                "element": "Air",
                "ruling_planet": "Uranus, Saturn",
                "image": "https://media-public.canva.com/IMnQU/MAEqYqIMnQU/1/t.png",
            },
            {
                "name": "Pisces",
                "symbol": "♓",
                "dateRange": "February 19 - March 20",
                "overview": "Intuitive and artistic, Pisces can easily escape into their dream world.",
                "element": "Water",
                "ruling_planet": "Neptune, Jupiter",
                "image": "https://media-public.canva.com/p-weY/MAEqYmp-weY/1/t.png",
            },
        ]
        for sign_data in data:
            try:
                zodiac_sign, created = ZodiacSigns.objects.update_or_create(
                    name=sign_data["name"],
                    defaults={
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

                # Download and save the image
                image_url = sign_data["image"]
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    image_content = ContentFile(response.content)
                    filename = f"{sign_data['name'].lower()}.png"
                    zodiac_sign.image.save(filename, image_content, save=True)
                    self.stdout.write(
                        self.style.SUCCESS(f"Saved image for {zodiac_sign.name}")
                    )
                except requests.RequestException as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Failed to download image for {zodiac_sign.name}: {e}"
                        )
                    )
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error saving image for {zodiac_sign.name}: {e}"
                        )
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
