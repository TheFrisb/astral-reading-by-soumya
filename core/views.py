from django.http import Http404
from django.views.generic import TemplateView, DetailView

from blog.services.BlogService import BlogService
from .mixins import PageTagsMixin
from .models import Horoscope, FrequentlyAskedQuestion
from .services.horoscopes_service import HoroscopeService
from .services.readings_service import ReadingsService
from .services.testimonials_service import TestimonialService


class HomeView(PageTagsMixin, TemplateView):
    template_name = "core/pages/horoscopes.html"
    page_title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horoscope_service = HoroscopeService()
        testimonial_service = TestimonialService()

        context["horoscope_signs"] = horoscope_service.get_horoscope_signs()
        context["testimonials"] = testimonial_service.get_active_testimonials()
        return context


class AboutView(PageTagsMixin, TemplateView):
    template_name = "core/pages/about.html"
    page_title = "About"


class ReadingsView(PageTagsMixin, TemplateView):
    template_name = "core/pages/readings.html"
    page_title = "Readings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        readings_service = ReadingsService()
        testimonials_service = TestimonialService()
        context["readings"] = readings_service.get_active_readings()
        context["testimonials"] = testimonials_service.get_active_testimonials()
        return context


class HoroscopeDetailView(DetailView):
    model = Horoscope
    template_name = "core/pages/horoscope_detail.html"
    context_object_name = "horoscope"

    def get_object(self, queryset=None):
        # Fetch the sign name from URL parameters
        sign_name = self.kwargs.get("sign_name")

        # Retrieve the filter type from request parameters (default to 'weekly')
        filter_type = self.request.GET.get("filter", "weekly").lower()

        # Validate filter_type to ensure it matches available frequencies
        valid_frequencies = [
            choice[0].lower() for choice in Horoscope.Frequency.choices
        ]
        if filter_type not in valid_frequencies:
            filter_type = "weekly"  # Default to 'weekly' if invalid

        service = HoroscopeService()
        horoscope = service.get_current_horoscope(sign_name, filter_type)

        if not horoscope:
            raise Http404("Horoscope does not exist")
        return horoscope

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_type = self.request.GET.get("filter", "weekly").lower()

        valid_frequencies = [
            choice[0].lower() for choice in Horoscope.Frequency.choices
        ]
        if filter_type not in valid_frequencies:
            filter_type = "weekly"

        filter_options = [
            {
                "label": "Weekly horoscope",
                "value": "weekly",
                "url": f"?filter=weekly",
                "active": filter_type == "weekly",
            },
            {
                "label": "Monthly horoscope",
                "value": "monthly",
                "url": f"?filter=monthly",
                "active": filter_type == "monthly",
            },
        ]

        service = HoroscopeService()
        blog_service = BlogService()
        context.update(
            {
                "filter_options": filter_options,
                "horoscope_signs": service.get_horoscope_signs(),
                "current_filter": filter_type,
                "related_blog_posts": blog_service.get_related_by_horoscope_sign(
                    self.object.sign
                ),
            }
        )
        return context


class FrequentlyAskedQuestionsView(PageTagsMixin, TemplateView):
    template_name = "core/pages/faq.html"
    page_title = "Frequently Asked Questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = FrequentlyAskedQuestion.objects.all()
        return context
