from datetime import date, timedelta

from django.db.models import QuerySet

from core.models import Horoscope, HoroscopeSign


class HoroscopeService:
    """
    Service class for Horoscope model
    """

    def get_current_horoscope(self, sign_name: str, frequency: str) -> Horoscope:
        """
        Get the current horoscope for a given sign and frequency.
        :param sign_name: Name of the horoscope sign.
        :param frequency: Frequency of the horoscope ('weekly' or 'monthly').
        :return: Horoscope object or None if not found.
        """
        frequency = frequency.upper()  # Normalize frequency to uppercase
        today = date.today()
        start_date, end_date = self._get_date_range(frequency)

        horoscope = Horoscope.objects.filter(
            sign__name__iexact=sign_name,
            frequency__iexact=frequency,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).first()
        return horoscope

    def _get_date_range(self, frequency: str):
        """
        Helper method to calculate the date range based on frequency.
        :param frequency: 'WEEKLY' or 'MONTHLY'
        :return: Tuple of (start_date, end_date)
        """
        today = date.today()

        if frequency == Horoscope.Frequency.WEEKLY:
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif frequency == Horoscope.Frequency.MONTHLY:
            start_date = today.replace(day=1)
            # Handle month transition
            if start_date.month == 12:
                end_date = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
        else:
            raise ValueError("Invalid frequency")
        return start_date, end_date

    def get_horoscope_signs(self) -> QuerySet:
        """
        Get all horoscope signs.
        :return: QuerySet of HoroscopeSign objects.
        """
        return HoroscopeSign.objects.all()
