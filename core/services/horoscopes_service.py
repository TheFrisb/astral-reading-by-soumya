from datetime import date, timedelta

from django.db.models import Prefetch, QuerySet

from core.models import Horoscope, HoroscopeSign


class HoroscopeService:
    """
    Service class for Horoscope model
    """

    def get_horoscope_signs(
        self, get_weekly_horoscope: bool = False, get_monthly_horoscope: bool = False
    ) -> QuerySet:
        """
        Get horoscope signs with weekly and monthly horoscopes for the current week and month
        :param get_weekly_horoscope: True if you want to get weekly horoscopes
        :param get_monthly_horoscope: True if you want to get monthly horoscopes
        :return: QuerySet of HoroscopeSign objects
        """
        today = date.today()

        # Calculate start and end of the current week
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Calculate start and end of the current month
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month.replace(
            month=start_of_month.month % 12 + 1, day=1
        ) - timedelta(days=1)

        # Prefetch weekly horoscopes for the current week
        weekly_horoscopes = Prefetch(
            "horoscopes",
            queryset=Horoscope.objects.filter(
                frequency=Horoscope.Frequency.WEEKLY,
                start_date__lte=end_of_week,
                end_date__gte=start_of_week,
            ),
            to_attr="weekly_horoscopes",
        )

        # Prefetch monthly horoscopes for the current month
        monthly_horoscopes = Prefetch(
            "horoscopes",
            queryset=Horoscope.objects.filter(
                frequency=Horoscope.Frequency.MONTHLY,
                start_date__lte=end_of_month,
                end_date__gte=start_of_month,
            ),
            to_attr="monthly_horoscopes",
        )

        # Fetch horoscope signs with filtered horoscopes
        horoscope_signs = HoroscopeSign.objects.prefetch_related(
            weekly_horoscopes if get_weekly_horoscope else None,
            monthly_horoscopes if get_monthly_horoscope else None,
        )

        return horoscope_signs
