import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from lorem.text import TextLorem

from core.models import Product, Testimonial


class Command(BaseCommand):
    help = "Creates 5 products, each with 10 testimonials"

    def handle(self, *args, **kwargs):
        lorem = TextLorem(
            wsep=" ", srange=(5, 10)
        )  # Configure lorem to generate sentences with 5-10 words
        product_types = [
            Product.Type.CALL_CONSULTATION,
            Product.Type.WRITTEN_REPORT,
        ]

        sample_names = [
            "John Doe",
            "Jane Smith",
            "Alice Johnson",
            "Bob Brown",
            "Charlie Davis",
        ]

        for i in range(5):
            # Create a product
            product = Product.objects.create(
                name=f"Product {i + 1}",
                type=random.choice(product_types),
                description=lorem.sentence(),  # Generate a lorem sentence for the description
                regular_price=Decimal(random.randint(50, 100)),
                discounted_price=(
                    Decimal(random.randint(20, 50))
                    if random.choice([True, False])
                    else None
                ),
            )
            self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))

            # Create 10 testimonials for the product
            for j in range(10):
                Testimonial.objects.create(
                    product=product,
                    name=random.choice(sample_names),
                    rating=random.randint(1, 5),
                    content=lorem.sentence(),  # Generate a lorem sentence for the testimonial content
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created 10 testimonials for product: {product.name}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Successfully created test data!"))
