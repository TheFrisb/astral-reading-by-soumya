from calendar import month_name, monthrange
from datetime import date

from django import forms

from core.models import Horoscope

# Create a list of tuples like [(1, "January"), (2, "February"), ...]
MONTH_CHOICES = [(i, month_name[i]) for i in range(1, 13)]


class HoroscopeForm(forms.ModelForm):
    year = forms.IntegerField(
        required=False, help_text="Needed for both Yearly and Monthly horoscopes."
    )
    month = forms.ChoiceField(
        required=False,
        choices=MONTH_CHOICES,
        help_text="Only needed for a monthly horoscope.",
    )

    class Meta:
        model = Horoscope
        fields = ["sign", "frequency", "content", "year", "month"]
        widgets = {
            "frequency": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)

        # If we have an existing instance, populate year and month if applicable
        if instance and instance.pk:
            if instance.frequency == instance.Frequency.YEARLY and instance.start_date:
                # For YEARLY, just extract the year from the start_date
                self.fields["year"].initial = instance.start_date.year
                # Clear the month since it's not needed for yearly
                self.fields["month"].initial = None

            elif (
                    instance.frequency == instance.Frequency.MONTHLY and instance.start_date
            ):
                # For MONTHLY, extract both year and month
                self.fields["year"].initial = instance.start_date.year
                self.fields["month"].initial = instance.start_date.month

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get("frequency")
        year = cleaned_data.get("year")
        month = cleaned_data.get("month")  # this will be a string from the choice

        if frequency == Horoscope.Frequency.YEARLY:
            if not year:
                self.add_error("year", "Year is required for a Yearly horoscope.")
            # Ignore month for yearly
            cleaned_data["month"] = None

        elif frequency == Horoscope.Frequency.MONTHLY:
            if not year:
                self.add_error("year", "Year is required for a Monthly horoscope.")
            if not month:
                self.add_error("month", "Month is required for a Monthly horoscope.")
            else:
                # Convert month from string to int
                month_int = int(month)
                if month_int < 1 or month_int > 12:
                    self.add_error("month", "Month must be between 1 and 12.")
                else:
                    cleaned_data["month"] = month_int

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        frequency = self.cleaned_data.get("frequency")
        year = self.cleaned_data.get("year")
        month = self.cleaned_data.get("month")

        if frequency == Horoscope.Frequency.YEARLY and year:
            # For YEARLY, cover the entire year
            instance.start_date = date(year, 1, 1)
            instance.end_date = date(year, 12, 31)

        elif frequency == Horoscope.Frequency.MONTHLY and year and month:
            # For MONTHLY, cover the entire month
            days_in_month = monthrange(year, month)[1]  # last day of the month
            instance.start_date = date(year, month, 1)
            instance.end_date = date(year, month, days_in_month)

        if commit:
            instance.save()

        return instance
