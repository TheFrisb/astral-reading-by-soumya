from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, activate
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Order
from .models import WorkDay, ScheduledAppointment
from .serializers import ScheduledAppointmentSerializer


class AvailableTimeSlotsView(APIView):
    def get(self, request, *args, **kwargs):
        date_str = request.query_params.get("date")
        order_id = request.query_params.get("order_id")

        # Activate UTC timezone
        activate("UTC")

        # Parse and validate the date
        if not date_str:
            raise ValidationError({"date": "This field is required."})
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError({"date": "Invalid date format. Use YYYY-MM-DD."})

        # Get the order and associated reading type
        try:
            order = Order.objects.get(id=order_id)
            reading_type = order.item.reading_type
            call_duration_minutes = reading_type.call_duration
        except Order.DoesNotExist:
            raise ValidationError({"order_id": "Invalid order ID."})
        except AttributeError:
            raise ValidationError(
                {
                    "order": "The order does not have a valid reading type with a call duration."
                }
            )

        # Validate call_duration
        if not call_duration_minutes:
            raise ValidationError(
                {
                    "reading_type": "The reading type does not have a valid call duration."
                }
            )

        call_duration = timedelta(minutes=call_duration_minutes)

        # Determine the workday for the given date
        day_of_week = date.strftime("%A")
        try:
            workday = WorkDay.objects.get(day=day_of_week)
        except WorkDay.DoesNotExist:
            return Response(
                {"detail": "No working hours configured for this day."}, status=404
            )

        # Generate start and end times for the workday in UTC
        start_of_day = make_aware(datetime.combine(date, workday.start_time))
        end_of_day = make_aware(datetime.combine(date, workday.end_time))

        # Fetch scheduled appointments
        appointments = ScheduledAppointment.objects.filter(
            start_time__gte=start_of_day, start_time__lt=end_of_day
        ).order_by("start_time")

        # Generate available timeslots
        available_timeslots = []
        current_time = start_of_day

        while current_time + call_duration <= end_of_day:
            next_time = current_time + call_duration
            # Check if the current timeslot overlaps with any appointments
            if not appointments.filter(
                    start_time__lt=next_time, end_time__gt=current_time
            ).exists():
                available_timeslots.append({"start": current_time, "end": next_time})
            current_time = next_time  # Move to the next non-overlapping slot

        # Return response with all times in UTC
        return Response(
            {
                "date": date_str,
                "day": day_of_week,
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
            serializer.save()
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
