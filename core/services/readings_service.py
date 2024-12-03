from core.models import Reading


class ReadingsService:
    """Readings Service class."""

    def get_active_readings(self):
        """Return a list of active readings."""
        return Reading.objects.filter(is_active=True).order_by("sortable_order")
