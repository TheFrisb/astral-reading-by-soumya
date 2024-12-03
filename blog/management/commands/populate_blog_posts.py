import random

import lorem
from django.core.management.base import BaseCommand

from blog.models import BlogPost
from core.models import HoroscopeSign


class Command(BaseCommand):
    help = "Create 50 blog posts with various horoscope tags."

    def handle(self, *args, **options):
        horoscope_signs = list(HoroscopeSign.objects.all())
        if not horoscope_signs:
            self.stdout.write(self.style.ERROR("No HoroscopeSign instances found."))
            return

        for i in range(50):
            title = lorem.sentence()
            # Generate a long content description
            content = [lorem.paragraph() for _ in range(random.randint(3, 10))]
            blog_post = BlogPost.objects.create(
                title=title, content="\n\n".join(content)
            )
            # Assign random horoscope signs to the blog post
            num_signs = random.randint(1, len(horoscope_signs))
            signs = random.sample(horoscope_signs, num_signs)
            blog_post.horoscopes.set(signs)
            blog_post.save()
            self.stdout.write(self.style.SUCCESS(f"Created BlogPost: {title}"))
