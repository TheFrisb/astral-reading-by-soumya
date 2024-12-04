from django import forms


class ConsultationForm(forms.Form):
    full_name = forms.CharField(
        label="Name",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter your Full Name"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your Email Address"}),
    )
    phone_number = forms.CharField(
        label="Phone",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Enter your Phone Number"}),
    )
    date_of_birth = forms.DateField(
        label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"})
    )
    place_of_birth_city = forms.CharField(
        label="Place of Birth City",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter your place of birth City"}),
    )
    place_of_birth_state = forms.CharField(
        label="Place of Birth State",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your place of birth State"}
        ),
    )
    time_of_birth = forms.TimeField(
        label="Time of Birth", widget=forms.TimeInput(attrs={"type": "time"})
    )
    am_pm = forms.ChoiceField(label="AM or PM", choices=[("AM", "AM"), ("PM", "PM")])
    consultation_call_type = forms.ChoiceField(
        label="Consultation Call Type",
        choices=[],  # Choices will be populated dynamically
    )
    reason_for_consultation = forms.CharField(
        label="Reason for Consultation",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Please describe your reason for seeking consultation"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        reading = kwargs.pop("reading", None)
        super().__init__(*args, **kwargs)

        if reading:
            reading_types = reading.variants.all()
            if reading_types.count() == 1:
                reading_type = reading_types.first()
                self.fields["consultation_call_type"].choices = [
                    (reading_type.pk, str(reading_type))
                ]
                self.fields["consultation_call_type"].initial = reading_type.pk
                self.fields["consultation_call_type"].widget.attrs["readonly"] = True
                self.fields["consultation_call_type"].widget.attrs["disabled"] = True

            else:
                choices = [(rt.pk, str(rt)) for rt in reading_types]
                self.fields["consultation_call_type"].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        # Ensure the consultation_call_type is set when field is disabled

        # check if full name is valid
        full_name = cleaned_data.get("full_name")

        return cleaned_data
