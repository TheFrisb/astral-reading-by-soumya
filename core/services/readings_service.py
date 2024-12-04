from core.models import Reading


class ReadingsService:
    """Readings Service class."""

    def get_active_readings(self):
        """Return a list of active readings."""
        return Reading.objects.filter(is_active=True).order_by("sortable_order")

    def get_reading_by_id(self, reading_id):
        """Return a reading by its ID."""
        return Reading.objects.filter(id=reading_id).first()
