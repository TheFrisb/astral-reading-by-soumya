import stripe
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView

from blog.services.BlogService import BlogService
from .forms.checkout_form import CheckoutForm
from .mixins import PageTagsMixin
from .models import Horoscope, FrequentlyAskedQuestion, ReadingType, Order, Reading
from .services.checkout.checkout_service import InternalCheckoutService
from .services.checkout.stripe_service import InternalStripeService
from .services.horoscopes_service import HoroscopeService
from .services.mail.mail_service import MailService
from .services.readings_service import ReadingsService
from .services.testimonials_service import TestimonialService


class HomeView(PageTagsMixin, TemplateView):
    template_name = "core/pages/home.html"
    page_title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horoscope_service = HoroscopeService()
        testimonial_service = TestimonialService()

        context.update(
            {
                "horoscope_signs": horoscope_service.get_horoscope_signs_with_current_horoscopes(),
                "testimonials": testimonial_service.get_active_testimonials(),
                "readings": Reading.objects.prefetch_related("variants")
                .all()
                .order_by("sortable_order"),
            }
        )

        return context


class HoroscopeListView(PageTagsMixin, TemplateView):
    template_name = "core/pages/horoscope_list.html"
    page_title = "Horoscopes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horoscope_service = HoroscopeService()
        context.update(
            {
                "horoscope_signs": horoscope_service.get_horoscope_signs_with_current_horoscopes(),
            }
        )

        return context


class CheckoutView(PageTagsMixin, FormView):
    template_name = "core/pages/checkout.html"
    page_title = "Checkout"
    form_class = CheckoutForm

    def get_reading(self):
        """Retrieve the Reading object based on the 'reading_id' URL parameter."""
        reading_id = self.kwargs.get("reading_id")
        readings_service = ReadingsService()
        reading = readings_service.get_reading_by_id(reading_id)
        if not reading:
            raise Http404("Reading does not exist")
        return reading

    def get_form_kwargs(self):
        """Pass the 'reading' object to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["reading"] = self.get_reading()
        return kwargs

    def get_context_data(self, **kwargs):
        """Add the 'reading' object to the context."""
        context = super().get_context_data(**kwargs)
        context["reading"] = self.get_reading()
        return context

    def form_valid(self, form):
        checkout_service = InternalCheckoutService()

        try:
            checkout_url = checkout_service.get_checkout_url(form)
        except ReadingType.DoesNotExist:
            form.add_error(
                "consultation_call_type", "Invalid consultation call type selected."
            )
            return self.form_invalid(form)

        return redirect(checkout_url)


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


class HoroscopeDetailView(PageTagsMixin, DetailView):
    model = Horoscope
    template_name = "core/pages/horoscope_detail.html"
    context_object_name = "horoscope"

    def get_object(self, queryset=None):
        sign_name = self.kwargs.get("sign_name")
        filter_type = self.request.GET.get("filter", "monthly").lower()  # Default to monthly
        valid_frequencies = [choice[0].lower() for choice in Horoscope.Frequency.choices]

        if filter_type not in valid_frequencies:
            filter_type = "monthly"

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
                "zodiac_signs": service.get_horoscope_signs(),
                "current_filter": filter_type,
                "related_blog_posts": blog_service.get_related_by_horoscope_sign(
                    self.object.sign
                ),
            }
        )
        return context

    def get_page_title(self):
        return f"{self.object.sign} Horoscope"


class FrequentlyAskedQuestionsView(PageTagsMixin, TemplateView):
    template_name = "core/pages/faq.html"
    page_title = "Frequently Asked Questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = FrequentlyAskedQuestion.objects.all().order_by(
            "sortable_order"
        )
        return context


class ThankYouView(PageTagsMixin, DetailView):
    template_name = "core/pages/thank_you.html"
    page_title = "Thank You"
    object = Order
    context_object_name = "order"

    def get_object(self, queryset=None):
        order_id = self.kwargs.get("order_id")

        try:
            order = (
                Order.objects.select_related("information", "item")
                .prefetch_related("item__reading_type", "item__reading_type__reading")
                .get(id=order_id)
            )
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        print(order.item.reading_type)

        mail_service = MailService()
        mail_service.send_mail(
            "bedzovski@yahoo.com",
            "Thank you for your order!",
            f"Thank you for your order! Your order ID is {order.id}.",
        )

        return order


class TimeSlotPickerView(PageTagsMixin, TemplateView):
    template_name = "core/pages/time_slot_picker.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@csrf_exempt
def stripe_webhook(request):
    stripe_service = InternalStripeService()
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe_service.process_stripe_event(payload, sig_header)
    except ValueError:
        # Invalid payload
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        print("Invalid signature")
        return HttpResponse("Invalid signature", status=400)

    return JsonResponse({"status": "success"})
