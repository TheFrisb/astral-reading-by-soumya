from django.core.management.base import BaseCommand

from blog.models import Category, BlogPost


class Command(BaseCommand):
    help = "Create 50 blog posts with various horoscope tags."

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
        categories = []
        for tag in data:
            obj = Category(name=tag["name"], symbol=tag["symbol"])
            obj.save()
            categories.append(obj)

        for category in categories:
            obj = BlogPost.objects.create(title="A blog post about " + category.name,
                                          content="This is a blog post about " + category.name)
            obj.categories.add(category)
            obj.save()
        self.stdout.write(self.style.SUCCESS("Successfully created 50 blog posts with various horoscope tags."))
        