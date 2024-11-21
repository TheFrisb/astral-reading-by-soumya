from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from core.forms.admin.horoscope_entry_form import HoroscopeForm
from core.models import HoroscopeSign, Product, Horoscope, FrequentlyAskedQuestion


class InternalBaseAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]


# Register your models here.
@admin.register(HoroscopeSign)
class HoroscopeSignAdmin(InternalBaseAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(InternalBaseAdmin):
    list_display = ("name", "type", "regular_price", "discounted_price")
    search_fields = ["name"]
    list_filter = ["type"]


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


admin.site.site_header = "Astrology Admin"
