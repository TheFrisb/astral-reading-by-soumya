from datetime import date, timedelta

from django.db.models import QuerySet, OuterRef, Subquery

from core.models import Horoscope, ZodiacSigns


class HoroscopeService:
    """
    Service class for Horoscope model
    """

    def get_current_horoscope(self, sign_name: str, frequency: str) -> Horoscope:
        """
        Get the current horoscope for a given sign and frequency.
        :param sign_name: Name of the horoscope sign.
        :param frequency: Frequency of the horoscope ('yearly' or 'monthly').
        :return: Horoscope object or None if not found.
        """
        frequency = frequency.upper()  # Normalize frequency to uppercase
        start_date, end_date = self._get_date_range(frequency)

        return Horoscope.objects.filter(
            sign__name__iexact=sign_name,
            frequency__iexact=frequency,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).first()

    def _get_date_range(self, frequency: str):
        """
        Helper method to calculate the date range based on frequency.
        :param frequency: 'YEARLY' or 'MONTHLY'
        :return: Tuple of (start_date, end_date)
        """
        today = date.today()

        if frequency == Horoscope.Frequency.YEARLY.value:
            # YEARLY: from Jan 1 to Dec 31 of the current year
            start_date = date(today.year, 1, 1)
            end_date = date(today.year, 12, 31)

        elif frequency == Horoscope.Frequency.MONTHLY.value:
            # MONTHLY: from the first day of this month to the last day of this month
            start_date = today.replace(day=1)
            if start_date.month == 12:
                # If December, next month is January of the next year
                end_date = start_date.replace(
                    year=start_date.year + 1, month=1, day=1
                ) - timedelta(days=1)
            else:
                # Otherwise, go to the first day of the next month and subtract one day
                end_date = start_date.replace(
                    month=start_date.month + 1, day=1
                ) - timedelta(days=1)
        else:
            raise ValueError("Invalid frequency. Must be 'monthly' or 'yearly'.")

        return start_date, end_date

    def get_horoscope_signs(self) -> QuerySet:
        """
        Get all horoscope signs.
        :return: QuerySet of ZodiacSigns objects.
        """
        return ZodiacSigns.objects.all().order_by("sortable_order")

    def get_horoscope_signs_with_current_horoscopes(self) -> QuerySet:
        """
        Get all horoscope signs with their current monthly and yearly horoscopes.
        :return: QuerySet of ZodiacSigns objects with current horoscopes attached.
        """
        today = date.today()

        # YEARLY range
        year_start = date(today.year, 1, 1)
        year_end = date(today.year, 12, 31)

        # MONTHLY range
        month_start = today.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(
                year=month_start.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            month_end = month_start.replace(
                month=month_start.month + 1, day=1
            ) - timedelta(days=1)

        # Subqueries to get current monthly and yearly horoscopes
        yearly_horoscope_subquery = (
            Horoscope.objects.filter(
                sign=OuterRef("pk"),
                frequency=Horoscope.Frequency.YEARLY,
                start_date__lte=year_end,
                end_date__gte=year_start,
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
        signs = ZodiacSigns.objects.annotate(
            current_yearly_horoscope_id=Subquery(yearly_horoscope_subquery),
            current_monthly_horoscope_id=Subquery(monthly_horoscope_subquery),
        ).order_by("sortable_order")

        signs = signs.order_by("sortable_order")

        # Collect all horoscope IDs
        horoscope_ids = set()
        for sign in signs:
            if sign.current_yearly_horoscope_id:
                horoscope_ids.add(sign.current_yearly_horoscope_id)
            if sign.current_monthly_horoscope_id:
                horoscope_ids.add(sign.current_monthly_horoscope_id)

        # Fetch all current horoscopes in one query
        horoscopes = Horoscope.objects.filter(id__in=horoscope_ids)
        horoscopes_by_id = {horoscope.id: horoscope for horoscope in horoscopes}

        # Attach horoscopes to signs
        for sign in signs:
            sign.current_yearly_horoscope = horoscopes_by_id.get(
                sign.current_yearly_horoscope_id
            )
            sign.current_monthly_horoscope = horoscopes_by_id.get(
                sign.current_monthly_horoscope_id
            )

        return signs
