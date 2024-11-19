from datetime import timedelta

from django import forms

from core.models import Horoscope


class HoroscopeForm(forms.ModelForm):
    class Meta:
        model = Horoscope
        fields = ["sign", "frequency", "start_date", "content"]
        widgets = {
            "start_date": forms.SelectDateWidget(),
            "frequency": forms.RadioSelect(),
        }

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get("frequency")
        start_date = cleaned_data.get("start_date")

        if frequency and start_date:
            if frequency == Horoscope.Frequency.WEEKLY:
                cleaned_data["end_date"] = start_date + timedelta(days=6)
            elif frequency == Horoscope.Frequency.MONTHLY:
                next_month = start_date.replace(day=28) + timedelta(days=4)
                cleaned_data["end_date"] = next_month - timedelta(days=next_month.day)
        return cleaned_data
