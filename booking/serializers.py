from rest_framework import serializers

from core.models import Order
from .models import ScheduledAppointment


class ScheduledAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledAppointment
        fields = ["start_time", "end_time", "order"]

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        order = data.get("order")

        # Ensure end_time is after start_time
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        # Ensure the order exists
        if not Order.objects.filter(
                id=order.id, status=Order.Status.COMPLETED
        ).exists():
            raise serializers.ValidationError("The provided order does not exist.")

        # Ensure the order does not already have an appointment
        if ScheduledAppointment.objects.filter(order=order).exists():
            raise serializers.ValidationError("This order already has an appointment.")

        # Ensure the time slot does not overlap with existing appointments
        overlapping_appointments = ScheduledAppointment.objects.filter(
            start_time__lt=end_time, end_time__gt=start_time
        )
        if overlapping_appointments.exists():
            raise serializers.ValidationError(
                "The selected time slot overlaps with an existing appointment."
            )

        return data
