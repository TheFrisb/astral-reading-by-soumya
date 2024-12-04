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
        # You can keep your existing clean method if you need validation here
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        frequency = self.cleaned_data.get("frequency")
        start_date = self.cleaned_data.get("start_date")

        if frequency and start_date:
            if frequency == Horoscope.Frequency.WEEKLY:
                instance.end_date = start_date + timedelta(days=6)
            elif frequency == Horoscope.Frequency.MONTHLY:
                next_month = start_date.replace(day=28) + timedelta(days=4)
                instance.end_date = next_month - timedelta(days=next_month.day)
        else:
            # Handle cases where frequency or start_date might be missing
            instance.end_date = None

        if commit:
            instance.save()
        return instance
