import re

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
    gender = forms.ChoiceField(
        label="Gender",
        choices=[("Male", "Male"), ("Female", "Female")],
        widget=forms.Select(),
    )
    birth_country = forms.CharField(
        label="Birth Country",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your Country of Birth",
                "id": "birth_country",
            }
        ),
    )
    birth_state = forms.CharField(
        label="Birth State",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your State of Birth",
                "id": "birth_state",
            }
        ),
    )
    birth_city = forms.CharField(
        label="Birth City",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your City of Birth",
                "id": "birth_city",
            }
        ),
    )
    time_of_birth = forms.CharField(
        label="Time of Birth",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your Time of Birth (HH:MM)",
                "id": "time_of_birth",
                "pattern": "^([0-1]?[0-9]|2[0-3]):[0-5]\\d$",  # Enforces HH:MM 24-hour format
                "maxlength": "5",
                "class": "time-input",
            }
        ),
    )
    day_part = forms.ChoiceField(label="AM or PM", choices=[("AM", "AM"), ("PM", "PM")])
    reading_type = forms.ChoiceField(
        label="Consultation Type",
        choices=[],
    )
    comment = forms.CharField(
        label="Reason for Consultation",
        required=True,
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

        time_of_birth = cleaned_data.get("time_of_birth")
        if time_of_birth:
            if not re.match(r"^([0-1]?[0-9]|2[0-3]):[0-5]\d$", time_of_birth):
                self.add_error(
                    "time_of_birth",
                    "Please enter a valid time in HH:MM format (24-hour clock).",
                )

        return cleaned_data
