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
    list_filter = ("sign", "frequency", "start_date")
    search_fields = ("sign__name", "content")
    date_hierarchy = "start_date"


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

    list_display = ("name", "is_active", "sortable_order")
    ordering = ("sortable_order",)
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines = [ReadingTypeInline]


admin.site.site_header = "Astrology Admin"
