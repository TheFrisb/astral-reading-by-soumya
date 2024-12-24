from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from solo.admin import SingletonModelAdmin

from core.forms.admin.horoscope_entry_form import HoroscopeForm
from core.models import (
    ZodiacSigns,
    Horoscope,
    FrequentlyAskedQuestion,
    ReadingType,
    Reading,
    Order,
    OrderInformation,
    OrderItem,
    Testimonial,
    HeroSection,
    SiteSettings,
    Location,
)
from core.services.mail.mail_service import MailService


class InternalBaseAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]


# Register your models here.
@admin.register(ZodiacSigns)
class HoroscopeSignAdmin(InternalBaseAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Horoscope)
class HoroscopeAdmin(InternalBaseAdmin):
    form = HoroscopeForm
    list_display = ("sign", "frequency", "start_date", "end_date")
    list_filter = ("sign", "frequency")
    search_fields = ("sign__name", "content")
    date_hierarchy = "start_date"
    readonly_fields = ["start_date", "end_date"] + InternalBaseAdmin.readonly_fields

    autocomplete_fields = ["sign"]


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(SortableAdminMixin, InternalBaseAdmin):
    list_display = ("question", "sortable_order")
    ordering = ("sortable_order",)


class ReadingTypeInline(admin.TabularInline):
    """
    Inline admin for managing Reading Types directly from the Reading admin.
    """

    model = ReadingType
    extra = 1
    max_num = ReadingType.Type.choices.__len__()


@admin.register(Reading)
class ReadingAdmin(SortableAdminMixin, InternalBaseAdmin):
    """
    Admin interface for Reading.
    """

    list_display = (
        "name",
        "is_active",
        "call_consultation",
        "written_report",
        "sortable_order",
    )
    ordering = ("sortable_order",)
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines = [ReadingTypeInline]

    # define the fields to be displayed in the list view
    def call_consultation(self, obj):
        return ReadingType.objects.filter(
            reading=obj, type=ReadingType.Type.CALL
        ).exists()

    def written_report(self, obj):
        return ReadingType.objects.filter(
            reading=obj, type=ReadingType.Type.REPORT
        ).exists()

    call_consultation.boolean = True
    written_report.boolean = True


# make orderInformation OneToOne inline
class OrderInformationInline(admin.StackedInline):
    model = OrderInformation
    readonly_fields = [f.name for f in OrderInformation._meta.fields]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = [f.name for f in OrderItem._meta.fields]


@admin.register(Order)
class OrderAdmin(InternalBaseAdmin):
    change_form_template = "admin/orders/order/change_form.html"
    list_display = ("id", "full_name", "item", "status", "created_at")
    list_filter = ("status",)
    search_fields = (
        "id",
        "information__full_name",
        "information__email",
    )
    date_hierarchy = "created_at"

    inlines = [OrderInformationInline, OrderItemInline]

    def full_name(self, obj):
        return obj.information.full_name

    def send_review_request(self, request, order_id):
        order = self.get_object(request, order_id)
        if order:
            mailer = MailService()
            try:
                mailer.send_leave_a_review_email(order.information.email, order)
                messages.success(request, f"Review request sent for Order {order.id}.")
            except Exception as e:
                messages.error(request, f"Error sending review request: {e}")
        else:
            messages.error(request, "Order not found.")
        return redirect("admin:core_order_change", object_id=order_id)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Ensure 'object' is passed to the template
        extra_context = extra_context or {}
        extra_context["object"] = self.get_object(request, object_id)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<uuid:order_id>/send-review-request/",
                self.admin_site.admin_view(self.send_review_request),
                name="order-send-review-request",
            ),
        ]
        return custom_urls + urls


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "content")
    autocomplete_fields = ["reading"]


admin.site.site_header = "Astrology Admin"
admin.site.register(HeroSection, SingletonModelAdmin)
admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Location, InternalBaseAdmin)
