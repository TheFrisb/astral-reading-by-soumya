from django.contrib import admin

from booking.models import WorkDay, ScheduledAppointment


# Register your models here.
@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ("day", "start_time", "end_time")


@admin.register(ScheduledAppointment)
class ScheduledAppointmentAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "get_reading_type")

    def get_reading_type(self, obj):
        return obj.order.item.reading_type.get_display_name

    get_reading_type.short_description = "Reading Type"
