from datetime import date, timedelta

from django.db.models import QuerySet, OuterRef, Subquery

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
                end_date = start_date.replace(
                    year=start_date.year + 1, month=1, day=1
                ) - timedelta(days=1)
            else:
                end_date = start_date.replace(
                    month=start_date.month + 1, day=1
                ) - timedelta(days=1)
        else:
            raise ValueError("Invalid frequency")
        return start_date, end_date

    def get_horoscope_signs(self) -> QuerySet:
        """
        Get all horoscope signs.
        :return: QuerySet of HoroscopeSign objects.
        """
        return HoroscopeSign.objects.all()

    def get_horoscope_signs_with_current_horoscopes(self) -> QuerySet:
        """
        Get all horoscope signs with their current weekly and monthly horoscopes.
        :return: QuerySet of HoroscopeSign objects with current horoscopes attached.
        """
        today = date.today()

        # Calculate current week start and end dates
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # Calculate current month start and end dates
        month_start = today.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(
                year=month_start.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            month_end = month_start.replace(
                month=month_start.month + 1, day=1
            ) - timedelta(days=1)

        # Subqueries to get current horoscopes
        weekly_horoscope_subquery = (
            Horoscope.objects.filter(
                sign=OuterRef("pk"),
                frequency=Horoscope.Frequency.WEEKLY,
                start_date__lte=week_end,
                end_date__gte=week_start,
            )
            .order_by("-start_date")
            .values("pk")[:1]
        )

        monthly_horoscope_subquery = (
            Horoscope.objects.filter(
                sign=OuterRef("pk"),
                frequency=Horoscope.Frequency.MONTHLY,
                start_date__lte=month_end,
                end_date__gte=month_start,
            )
            .order_by("-start_date")
            .values("pk")[:1]
        )

        # Annotate signs with current horoscope IDs
        signs = HoroscopeSign.objects.annotate(
            current_weekly_horoscope_id=Subquery(weekly_horoscope_subquery),
            current_monthly_horoscope_id=Subquery(monthly_horoscope_subquery),
        )

        # Collect all horoscope IDs
        horoscope_ids = set()
        for sign in signs:
            if sign.current_weekly_horoscope_id:
                horoscope_ids.add(sign.current_weekly_horoscope_id)
            if sign.current_monthly_horoscope_id:
                horoscope_ids.add(sign.current_monthly_horoscope_id)

        # Fetch all current horoscopes in one query
        horoscopes = Horoscope.objects.filter(id__in=horoscope_ids)
        horoscopes_by_id = {horoscope.id: horoscope for horoscope in horoscopes}

        # Attach horoscopes to signs
        for sign in signs:
            sign.current_weekly_horoscope = horoscopes_by_id.get(
                sign.current_weekly_horoscope_id
            )
            sign.current_monthly_horoscope = horoscopes_by_id.get(
                sign.current_monthly_horoscope_id
            )

        return signs
