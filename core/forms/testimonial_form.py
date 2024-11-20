from django import forms

from core.models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["full_name", "rating", "content"]

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if not rating or rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
