from django.contrib import admin
from imagekit.admin import AdminThumbnail

from core.forms.admin.horoscope_entry_form import HoroscopeForm
from core.models import HoroscopeSign, Product, Horoscope


class InternalBaseAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]


# Register your models here.
@admin.register(HoroscopeSign)
class HoroscopeSignAdmin(InternalBaseAdmin):
    list_display = ["name", "admin_thumbnail"]
    search_fields = ["name"]
    admin_thumbnail = AdminThumbnail(image_field="processed_webp")


@admin.register(Product)
class ProductAdmin(InternalBaseAdmin):
    list_display = ("name", "type", "regular_price", "discounted_price")
    search_fields = ["name"]
    list_filter = ["type"]


@admin.register(Horoscope)
class HoroscopeAdmin(admin.ModelAdmin):
    form = HoroscopeForm
    list_display = ("sign", "frequency", "start_date", "end_date")
    list_filter = ("sign", "frequency", "start_date")
    search_fields = ("sign__name", "content")
    date_hierarchy = "start_date"


admin.site.site_header = "Astrology Admin"
