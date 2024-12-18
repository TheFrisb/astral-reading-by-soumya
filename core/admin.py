from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
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
)


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


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "content")
    autocomplete_fields = ["reading"]


admin.site.site_header = "Astrology Admin"
admin.site.register(HeroSection, SingletonModelAdmin)
