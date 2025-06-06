from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from django.utils import timezone
from solo.admin import SingletonModelAdmin

from booking.models import ScheduledAppointment
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
    Location,
    SiteSettings,
    AboutUsSettings, AboutUsSectionCard, AboutUsSection,
)
from core.services.mail.mail_service import MailService


class InternalBaseAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]


# Register your models here.
@admin.register(ZodiacSigns)
class ZodiacSignAdmin(SortableAdminMixin, InternalBaseAdmin):
    list_display = ["name", "sortable_order"]
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

    class Media:
        css = {"all": ("css/admin/custom_admin.css",)}


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


class OrderInformationInline(admin.StackedInline):
    model = OrderInformation
    can_delete = False
    # extra = 0
    max_num = 1

    # readonly_fields = [
    #     "full_name",
    #     "email",
    #     "phone_number",
    #     "date_of_birth",
    #     "place_of_birth",
    #     "time_of_birth",
    #     "day_part",
    #     "comment",
    # ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    can_delete = False
    # extra = 0
    max_num = 1

    # readonly_fields = [
    #     "reading_type",
    #     "quantity",
    #     "price",
    #     "get_total_price",
    # ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ScheduledAppointmentInline(admin.StackedInline):
    model = ScheduledAppointment
    can_delete = False
    extra = 0
    max_num = 1
    readonly_fields = [
        "start_time",
        "end_time",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ConsultationTypeFilter(admin.SimpleListFilter):
    """
    Filter orders by the ReadingType type (CALL or REPORT).
    """

    title = "Consultation Type"
    parameter_name = "consultation_type"

    def lookups(self, request, model_admin):
        # Return ReadingType.Type choices as filter options
        return ReadingType.Type.choices

    def queryset(self, request, queryset):
        if self.value() in [choice[0] for choice in ReadingType.Type.choices]:
            return queryset.filter(item__reading_type__type=self.value())
        return queryset


class FutureAppointmentFilter(admin.SimpleListFilter):
    """
    Filter orders that have future appointments scheduled.
    """

    title = "Future Appointment"
    parameter_name = "future_appointment"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has future appointment"),
            ("no", "Does not have future appointment"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            # Show only Orders whose appointment starts in the future
            return queryset.filter(appointment__start_time__gte=timezone.now())
        elif self.value() == "no":
            # Show only Orders that do not have a future appointment
            return queryset.exclude(appointment__start_time__gte=timezone.now())
        return queryset


@admin.register(Order)
class OrderAdmin(InternalBaseAdmin):
    change_form_template = "admin/orders/order/change_form.html"
    list_display = (
        "id",
        "order_full_name",
        "reading_type_display_name",
        "scheduled_appointment",
        "created_at",
    )
    list_filter = (ConsultationTypeFilter, FutureAppointmentFilter)
    inlines = [OrderInformationInline, OrderItemInline, ScheduledAppointmentInline]
    ordering = ("-created_at",)

    search_fields = (
        "id",
        "information__full_name",
        "information__email",
    )
    date_hierarchy = "created_at"

    def send_review_request(self, request, order_id):
        order = self.get_object(request, order_id)
        if order:
            mailer = MailService()
            try:
                mailer.send_leave_a_review_email(order.information.email, order)
                messages.success(request, f"Review request sent for Order {order.id}.")
            except Exception as e:
                print(f"Error sending review request: {e}")
                # print stack trace for debugging
                import traceback

                traceback.print_exc()
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

    def get_queryset(self, request):
        """
        Override the default queryset to show only CONFIRMED orders.
        """
        qs = super().get_queryset(request)
        return qs.filter(status=Order.Status.COMPLETED)

    @admin.display(description="Full Name")
    def order_full_name(self, obj):
        """
        Safely retrieve the full_name from OrderInformation.
        """
        if hasattr(obj, "information"):
            return obj.information.full_name
        return "-"

    @admin.display(description="Reading Type")
    def reading_type_display_name(self, obj):
        """
        Safely retrieve the reading type display name.
        """
        if hasattr(obj, "item") and obj.item.reading_type:
            return obj.item.reading_type.get_display_name
        return "-"

    @admin.display(description="Scheduled Appointment")
    def scheduled_appointment(self, obj):
        """
        Show the appointment times if this is a CALL consultation.
        Otherwise, display '-'.
        """
        # Ensure the order has an item, reading_type, and an appointment.
        if (
            hasattr(obj, "item")
            and hasattr(obj, "appointment")
            and obj.item.reading_type.type == ReadingType.Type.CALL
        ):
            local_start = timezone.localtime(obj.appointment.start_time)
            local_end = timezone.localtime(obj.appointment.end_time)
            return f"{local_start.strftime('%Y-%m-%d %I:%M %p %Z')} - {local_end.strftime('%Y-%m-%d %I:%M %p %Z')}"
        return "-"

    @admin.display(description="Created At")
    def created_at(self, obj):
        return obj.created_at


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    search_fields = ["reading_type__reading__name", "reading_type__type"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("full_name", "reading_type", "is_active")
    list_filter = ("is_active", "reading_type")
    search_fields = ("full_name", "content")

    autocomplete_fields = ["order_item"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    model = SiteSettings

    fieldsets = (
        (
            "Email Configuration",
            {
                "fields": ("thank_you_template_id", "leave_a_review_template_id"),
            },
        ),
        (
            "Hero Section Configuration",
            {
                "fields": ("hero_title", "hero_subtitle", "hero_background_image"),
            },
        ),
        (
            "Video Section Configuration",
            {
                "fields": (
                    "show_video_section",
                    "video_section_header",
                    "video_section_header_subtitle",
                    "video_section_video",
                    "video_section_video_thumbnail",
                    "video_section_description_header",
                    "video_section_description_header_subtitle",
                ),
            },
        ),
    )


class AboutUsSectionCardInline(SortableInlineAdminMixin, admin.StackedInline):
    model = AboutUsSectionCard
    extra = 1
    ordering = ['sortable_order']
    fieldsets = (
        ('Card Content', {
            'fields': ('title', 'description', 'image'),
        }),
        ('Order', {
            'fields': ('sortable_order',),
        }),
    )


@admin.register(AboutUsSettings)
class AboutUsSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Header Image', {
            'fields': ('personal_picture',),
        }),
        ('Info Cards', {
            'fields': (
                'card_info_1_title',
                'card_info_1_description',
                'card_info_2_title',
                'card_info_2_description',
                'card_info_3_title',
                'card_info_3_description',
            )
        }),
        ('Section 1', {
            'fields': ('section_1_header', 'section_1_description'),
        }),
        ('Section 2', {
            'fields': ('section_2_header', 'section_2_description'),
        }),
        ('Inspirational Quote', {
            'fields': ('inspirational_quote',),
        }),
        ('Section 3', {
            'fields': ('section_3_header', 'section_3_description'),
        }),
        ('Contact Information', {
            'fields': ('email', 'instagram', 'phone_number'),
        }),
    )


@admin.register(AboutUsSection)
class AboutUsSectionAdmin(SortableAdminMixin, InternalBaseAdmin):
    list_display = ('title', 'sortable_order')
    ordering = ['sortable_order']
    fieldsets = (
        ('Section Details', {
            'fields': ('title',),
        }),
        ('Order', {
            'fields': ('sortable_order',),
        }),
    )
    readonly_fields = ["sortable_order"]
    inlines = [AboutUsSectionCardInline]

admin.site.site_header = "Astrology Admin"
admin.site.register(Location, InternalBaseAdmin)
admin.site.register(OrderInformation)
