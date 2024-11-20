from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, activate
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Order
from core.services.mail.mail_service import MailService
from .models import WorkDay, ScheduledAppointment
from .serializers import ScheduledAppointmentSerializer


class AvailableTimeSlotsView(APIView):
    def get(self, request, *args, **kwargs):
        date_str = request.query_params.get("date", None)
        order_id = request.query_params.get("order_id", None)

        if not date_str:
            raise ValidationError({"date": "This field is required."})
        if not order_id:
            raise ValidationError({"order_id": "This field is required."})

        activate("America/Los_Angeles")

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError({"date": "Invalid date format. Use YYYY-MM-DD."})

        try:
            order = Order.objects.get(id=order_id, status=Order.Status.COMPLETED)
            reading_type = order.item.reading_type
            call_duration_minutes = reading_type.call_duration
            if not call_duration_minutes or call_duration_minutes <= 0:
                raise ValidationError({"call_duration": "Invalid call duration."})
        except Order.DoesNotExist:
            raise ValidationError({"order_id": "Invalid order ID."})
        except AttributeError:
            raise ValidationError({"order": "Invalid reading type configuration."})

        call_duration = timedelta(minutes=call_duration_minutes)

        try:
            workday = WorkDay.objects.get(day__iexact=date.strftime("%A"))
        except WorkDay.DoesNotExist:
            return Response(
                {"detail": "No working hours configured for this day."}, status=404
            )

        start_of_day = make_aware(datetime.combine(date, workday.start_time))
        end_of_day = make_aware(datetime.combine(date, workday.end_time))

        appointments = ScheduledAppointment.objects.filter(
            start_time__gte=start_of_day, start_time__lt=end_of_day
        ).order_by("start_time")

        available_timeslots = []
        current_time = start_of_day

        for appointment in appointments:
            while current_time + call_duration <= appointment.start_time:
                next_time = current_time + call_duration
                available_timeslots.append({"start": current_time, "end": next_time})
                current_time = next_time

            current_time = max(current_time, appointment.end_time)
        while current_time + call_duration <= end_of_day:
            next_time = current_time + call_duration
            available_timeslots.append({"start": current_time, "end": next_time})
            current_time = next_time

        return Response(
            {
                "date": date_str,
                "day": date.strftime("%A"),
                "call_duration": f"{call_duration_minutes} minutes",
                "available_timeslots": [
                    {"start": slot["start"].isoformat(), "end": slot["end"].isoformat()}
                    for slot in available_timeslots
                ],
            }
        )


class ScheduledAppointmentCreateView(APIView):
    """
    API endpoint for creating ScheduledAppointment instances.
    """

    def post(self, request, *args, **kwargs):
        serializer = ScheduledAppointmentSerializer(data=request.data)

        if serializer.is_valid():
            scheduled_appointment = serializer.save()
            mailer = MailService()
            mailer.send_booking_notification_email(scheduled_appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAppointmentView(TemplateView):
    template_name = "booking/book.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the order by UUID from the URL
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        context["order"] = order
        context["has_appointment"] = hasattr(order, "appointment")
        return context
