from django.db.models.query import QuerySet

from core.models import Testimonial


class TestimonialService:
    """
    Service class for handling testimonials.

    """

    def get_active_testimonials(self) -> QuerySet:
        """
        Retrieves all active testimonials.

        Returns: QuerySet: A queryset of active testimonials.
        """
        return Testimonial.objects.filter(is_active=True).select_related("product")[0:5]