import lorem
from django.core.management.base import BaseCommand

from core.models import FrequentlyAskedQuestion


class Command(BaseCommand):
    help = "Populate the database with 15 frequently asked questions"

    def handle(self, *args, **kwargs):
        for i in range(15):
            question = lorem.sentence() + "?"
            answer = lorem.paragraph()
            faq = FrequentlyAskedQuestion.objects.create(
                question=question, answer=answer, sortable_order=i
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created FAQ: {faq.question}")
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated FAQs"))
