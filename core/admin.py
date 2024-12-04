from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from core.forms.admin.horoscope_entry_form import HoroscopeForm
from core.models import (
    HoroscopeSign,
    Horoscope,
    FrequentlyAskedQuestion,
    ReadingType,
    Reading,
)


class InternalBaseAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]


# Register your models here.
@admin.register(HoroscopeSign)
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
    readonly_fields = ["end_date"] + InternalBaseAdmin.readonly_fields


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


admin.site.site_header = "Astrology Admin"
