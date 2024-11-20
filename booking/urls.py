from django.urls import path

from booking.views import AvailableTimeSlotsView, BookAppointmentView, ScheduledAppointmentCreateView

app_name = "booking"
urlpatterns = [
    path("get-time-slots/", AvailableTimeSlotsView.as_view(), name="get_time_slots"),
    path(
        "book/<uuid:order_id>/", BookAppointmentView.as_view(), name="book_appointment"
    ),
    path("create-appointment/", ScheduledAppointmentCreateView.as_view(), name="create_appointment"),
]
