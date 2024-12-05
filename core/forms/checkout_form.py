from django import forms

from core.models import Reading


class CheckoutForm(forms.Form):
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
    birth_city = forms.CharField(
        label="Place of Birth City",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter your place of birth City"}),
    )
    birth_state = forms.CharField(
        label="Place of Birth State",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your place of birth State"}
        ),
    )
    time_of_birth = forms.TimeField(
        label="Time of Birth", widget=forms.TimeInput(attrs={"type": "time"})
    )
    day_part = forms.ChoiceField(label="AM or PM", choices=[("AM", "AM"), ("PM", "PM")])
    reading_type = forms.ChoiceField(
        label="Consultation Call Type",
        choices=[],
    )
    comment = forms.CharField(
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
            self.populate_reading_choices(reading)
        else:
            raise ValueError("Reading object is required")

    def populate_reading_choices(self, reading: Reading) -> None:
        """
        Yea, this is a docstring.
        """
        reading_types = reading.variants.all()
        if reading_types.count() > 1:
            choices = [(rt.pk, str(rt)) for rt in reading_types]
            self.fields["reading_type"].choices = choices
        else:
            reading_type = reading_types.first()
            self.fields["reading_type"].choices = [(reading_type.pk, str(reading_type))]
            self.fields["reading_type"].initial = [reading_type.pk]
            self.fields["reading_type"].widget.attrs["readonly"] = True
            self.fields["reading_type"].widget.attrs["style"] = "pointer-events: none;"

    def clean(self):
        cleaned_data = super().clean()

        full_name = cleaned_data.get("full_name")
        if len(full_name.split(" ")) < 2:
            self.add_error("full_name", "Please enter your full name.")

        return cleaned_data
